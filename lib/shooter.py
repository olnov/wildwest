import pygame
import os


class Shooter:
    def __init__(self, x, y, idle_folder, shoot_folder, flip=False):
        self.x = x
        self.y = y

        # Load idle and shooting frames
        self.idle_frames = self.load_frames(idle_folder,flip)
        self.shooting_frames = self.load_frames(shoot_folder,flip)

        # Debug print to verify frames are loaded
        print(f"Idle frames loaded: {len(self.idle_frames)} from {idle_folder}")
        print(f"Shooting frames loaded: {len(self.shooting_frames)} from {shoot_folder}")

        # Set initial animation state
        self.current_frames = self.idle_frames
        self.current_frame = 0
        self.animation_speed = 20  # Lower value = faster animation
        self.frame_counter = 0

        # Shooting state
        self.shooting = False
        self.shooting_timer = 0
        self.shooting_duration = 20  # Frames to display the shooting animation


    def load_frames(self, folder, flip=False):
        """
        Load all frames from the specified folder.
        Frames should be PNG files with transparency.
        """
        frames = []
        for file_name in sorted(os.listdir(folder)):
            if file_name.endswith(".png"):  # Ensure only PNG files are loaded
                frame_path = os.path.join(folder, file_name)
                frame = pygame.image.load(frame_path).convert_alpha()
                if flip:  # Flip the frame horizontally if needed
                    frame = pygame.transform.flip(frame, True, False)
                frames.append(frame)
        if not frames:
            raise FileNotFoundError(f"No valid images found in folder: {folder}")
        return frames

    def update(self):
        """
        Update the animation state for the shooter.
        Handles frame cycling and transitions between idle and shooting animations.
        """
        if self.shooting:
            self.shooting_timer += 1
            if self.shooting_timer >= self.shooting_duration:
                self.shooting = False
                self.shooting_timer = 0
                self.current_frames = self.idle_frames  # Return to idle animation

        # Update frame counter for animations
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)

    def shoot(self):
        """
        Trigger the shooting animation.
        Switches to the shooting frames and resets the frame index.
        """
        self.shooting = True
        self.current_frames = self.shooting_frames
        self.current_frame = 0
        print("Shooting animation triggered.")

    def draw(self, surface):
        """
        Draw the current frame of the shooter to the provided surface.
        """
        if self.current_frames:
            surface.blit(self.current_frames[self.current_frame], (self.x, self.y))
