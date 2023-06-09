import pygame
import sys

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('Graphics/background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

transfer_sound = pygame.mixer.Sound(f"Sounds/water_transfer.wav")
victory_sound = pygame.mixer.Sound("Sounds/victory.wav")
victory_image = pygame.image.load("Graphics/victory.png")
victory_image = pygame.transform.scale(victory_image, (200, 200))  # Adjust the image size as desired
victory_image_rect = victory_image.get_rect(center=(screen_width // 2, screen_height // 2))  # Position the image at the center of the screen


class Bucket:
    def __init__(self, capacity, x, y):
        self.capacity = capacity
        self.amount = 0
        self.x = x
        self.y = y
        self.highlighted = False
        self.scale_param = 35
        self.image = pygame.image.load(f'Graphics/{capacity}_0.png')
        self.image = pygame.transform.scale(self.image, (80, capacity * self.scale_param))  # Scale the image
        # Update the rect dimensions to match the image's dimensions
        self.rect = pygame.Rect(x, y - capacity * self.scale_param, self.image.get_width(), self.image.get_height())

    def is_full(self):
        return self.amount == self.capacity

    def is_empty(self):
        return self.amount == 0

    def refresh_image(self):
        self.image = pygame.image.load(f'Graphics/{self.capacity}_{self.amount}.png')
        self.image = pygame.transform.scale(self.image, (80, self.capacity * self.scale_param))
        # Update the rect dimensions to match the image's dimensions
        self.rect = pygame.Rect(self.x, self.y - self.capacity * self.scale_param, self.image.get_width(), self.image.get_height())

    def fill(self, amount):
        self.amount = min(self.amount + amount, self.capacity)
        self.refresh_image()  # Update the image when the bucket is filled

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y - self.rect.height))


class StateGraph:
    def __init__(self, screen):
        self.nodes = []
        self.edges = []
        self.screen = screen
        self.font = pygame.font.SysFont(None, 20)

    def add_node(self, state):
        if state not in [node["state"] for node in self.nodes]:
            x, y = self.get_custom_position(state)
            self.nodes.append({
                "state": state,
                "x": x,
                "y": y
            })

    def add_edge(self, state1, state2):
        self.edges.append((state1, state2))

    def draw(self):
        for edge in self.edges:
            state1, state2 = edge
            x1, y1 = self.get_position_of_state(state1)
            x2, y2 = self.get_position_of_state(state2)
            pygame.draw.line(self.screen, (0, 0, 255), (x1, y1), (x2, y2), 2)

        for node in self.nodes:
            x, y = node["x"], node["y"]
            pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 20)
            text = self.font.render(str(node["state"]), True, (0, 0, 0))
            self.screen.blit(text, (x - 10, y - 10))

    def get_position_of_state(self, state):
        for node in self.nodes:
            if node["state"] == state:
                return node["x"], node["y"]
        return None

    def get_custom_position(self, state):
        # Customize the positions of certain states
        screen_width, screen_height = screen.get_size()
        positions = {
            (8, 0, 0): (500, 370),
            (5, 0, 3): (600, 370),
            (3, 5, 0): (500, 270),
            (0, 5, 3): (600, 270)
        }

        if state in positions:
            return positions[state]

        # For other states, position them linearly (as example)
        return len(self.nodes) * 100 + 50, screen_height // 2


def update(self):
    # Update the graph when the user pours water between the buckets
    def pour_water(source, target, graph):
        amount = min(source.amount, target.capacity - target.amount)
        source.amount -= amount
        target.fill(amount)
        graph.update()




buckets = [
    Bucket(8, 50, 500),
    Bucket(5, 180, 500),
    Bucket(3, 310, 500)
]

buckets[0].fill(8)
buckets[1].fill(0)
buckets[2].fill(0)


selected_bucket = None
transfer_options = []
history = []
current_state_label = pygame.font.SysFont(None, 24)
bucket_amounts_label = pygame.font.SysFont(None, 24)
state_history = []
mouse_pos = pygame.mouse.get_pos()  # Move the mouse_pos declaration before the event loop
state_graph = StateGraph(screen)

while True:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
            hovered_bucket = None
            for bucket in buckets:
                if bucket.rect.colliderect(mouse_rect):
                    bucket.highlighted = True
                    # Check if the bucket is not empty
                    if bucket.amount > 0:
                        hovered_bucket = bucket
                else:
                    bucket.highlighted = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
            mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

            for bucket in buckets:
                if bucket.rect.colliderect(mouse_rect):
                    if bucket.amount == 0:
                        continue
                    # The user clicked on the current bucket
                    selected_bucket = bucket
                    # Get transfer options for the selected bucket
                    transfer_options = [b for b in buckets if b != selected_bucket and not b.is_full()]

            # Check if the user clicked on a transfer option in the popup
            if selected_bucket and transfer_options:
                popup_x = selected_bucket.x + 30
                popup_y = selected_bucket.y - 30 * len(transfer_options)
                option_clicked = (mouse_pos[0] >= popup_x and mouse_pos[0] <= popup_x + 150 and
                                  mouse_pos[1] >= popup_y and mouse_pos[1] <= popup_y + 30 * len(transfer_options))
                if option_clicked:
                    transfer_sound.play()

                    option_index = (mouse_pos[1] - popup_y) // 30
                    destination_bucket = transfer_options[option_index]
                    amount_to_transfer = min(selected_bucket.amount,
                                             destination_bucket.capacity - destination_bucket.amount)
                    selected_bucket.amount -= amount_to_transfer
                    destination_bucket.fill(amount_to_transfer)
                    selected_bucket = None  # Reset the selected bucket
                    # history.append((selected_bucket, destination_bucket, amount_to_transfer))
                    # state_history.append(tuple(bucket.amount for bucket in buckets))
                    for bucket in buckets:
                        print(f"Bucket {bucket.capacity}: {bucket.amount} liters")
                    print(state_history)

                    if any(bucket.amount == 4 for bucket in buckets):
                        victory_sound.play()  # Play the victory sound
                        screen.blit(victory_image, victory_image_rect)  # Display the victory image
                        pygame.display.flip()  # Update the display to show the image
                        pygame.time.delay(3000)  # Delay for 3 seconds before continuing
                        print('Victory!')

    # Handle user input for pouring water
    mouse_pos = pygame.mouse.get_pos()
    # Create a small rect for the mouse
    mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

    # Redraw the screen
    #screen.fill((233, 255, 249))
    for bucket in buckets:
        if bucket.rect.colliderect(mouse_rect):
            bucket.highlighted = True
        else:
            bucket.highlighted = False

        main_capacity_text = str(bucket.amount)
        main_capacity_surface = pygame.font.SysFont(None, 24).render(main_capacity_text, True, (0, 0, 0))
        main_capacity_rect = main_capacity_surface.get_rect(
            center=(bucket.x + 40, bucket.y - bucket.capacity * bucket.scale_param))
        screen.blit(main_capacity_surface, main_capacity_rect)

        rect_color = (192, 192, 192) if bucket.rect.collidepoint(mouse_pos) else (128, 128, 128)
        #pygame.draw.rect(screen, rect_color, bucket.rect)

        bucket.draw(screen)
        bucket.refresh_image()



    current_state_text = ', '.join(str(bucket.amount) for bucket in buckets)
    current_state_surface = current_state_label.render(f"Current State: {current_state_text}", True, (0, 0, 0))
    screen.blit(current_state_surface, (20, 20))

    state_graph.draw()

    # Display bucket amounts
    for i, _prev_state in enumerate(state_history):
        bucket_amounts_text = str(_prev_state)
        bucket_amounts_surface = bucket_amounts_label.render(bucket_amounts_text, True, (0, 0, 0))
        screen.blit(bucket_amounts_surface, (700, 50 + i * 30))

    # Draw transfer options popup if a bucket is selected
    if hovered_bucket:
        popup_width = 100
        popup_height = 30 * len(transfer_options)
        popup_x = hovered_bucket.x + 30
        popup_y = hovered_bucket.y - popup_height
        pygame.draw.rect(screen, (255, 255, 255), (popup_x, popup_y, popup_width, popup_height))
        for i, option in enumerate(transfer_options):
            option_text = f"Bucket {option.capacity}"
            option_rect = pygame.Rect(popup_x, popup_y + 30 * i, popup_width, 30)
            pygame.draw.rect(screen, (200, 200, 200), option_rect)
            font = pygame.font.SysFont(None, 24)
            text = font.render(option_text, True, (0, 0, 0))
            text_rect = text.get_rect(center=option_rect.center)
            screen.blit(text, text_rect)

        new_state = tuple(bucket.amount for bucket in buckets)
        state_graph.add_node(new_state)
        state_graph.draw()
        # if state_history:
        #     prev_state = state_history[-1]
        #     state_graph.add_edge(prev_state, new_state)
        # state_history.append(new_state)
    #pygame.draw.circle(screen, (0, 255, 0), (500, 370), 20)
    pygame.display.flip()
