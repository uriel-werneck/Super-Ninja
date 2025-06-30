import pgzrun
import math

# Configurações do jogo
WIDTH = 800
HEIGHT = 600
TITLE = "Super Ninja"
GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_STRENGTH = 20

# Variaveis do jogo
game_state = "Menu"
is_muted = False

# Botões
buttons = [
    {"label": "Start", "rect": Rect((WIDTH//2 - 100, 250), (200, 60)), "action": "start"},
    {"label": "Mute", "rect": Rect((WIDTH//2 - 100, 330), (200, 60)), "action": "mute"},
    {"label": "Quit", "rect": Rect((WIDTH//2 - 100, 410), (200, 60)), "action": "quit"},
]

# Atores
menu_background = Actor("wood", (WIDTH//2, HEIGHT//2))
game_background = Actor("grass_field", (WIDTH//2, HEIGHT//2))
platform = Actor("platform", (WIDTH//2, HEIGHT//2))  # Adjust Y as needed

# classes
class Human(Actor):
    def __init__(self, name: str, default_anim: str, pos: tuple):
        super().__init__(default_anim, pos)
        self.name = name
        self.vx = 0
        self.vy = 0
        self.is_attacking = False
        self.x_target_1 = 0
        self.x_target_2 = 0
        self.reach_target_1 = False
        self.reach_target_2 = False
        self.rest_delay = 60  # Tempo de descanso em frames
        self.current_rest_delay = 0
        self.on_rest_delay = True
        self.dead = False
        self.on_ground = False
        self.is_attacking = False
        self.dead = False
        self.anim_state = "idle"
        self.anim_frame = 1
        self.anim_timer = 0

# Variáveis do jogador
player = Human("player", "player_idle_1", (50, HEIGHT - 30))

# Váriaveis do inimigo1
enemy1 = Human("enemy", "enemy_idle_1", (WIDTH - 300, HEIGHT - 30))
enemy1.y = HEIGHT - 30 - enemy1.height // 2
enemy1.x_target_1 = enemy1.x + 150
enemy1.x_target_2 = enemy1.x

# Váriaveis do inimigo2
enemy2 = Human("enemy", "enemy_idle_1", (WIDTH//2, HEIGHT - 30))
enemy2.y = HEIGHT//2 - enemy2.height // 2 - platform.height // 2
enemy2.x_target_1 = platform.x + platform.width // 2 - enemy2.width // 2
enemy2.x_target_2 = platform.x - platform.width // 2 + enemy2.width // 2

# Função para atualizar a animação do ator
def update_actor_animation(actor, total_idle_frames, total_walk_frames, total_attack_frames, total_dead_frames):
    # Escolhe o estado de animação
    if actor.dead:
        if actor.anim_state != "dead":
            actor.anim_state = "dead"
            actor.anim_frame = 1
            actor.anim_timer = 0
    elif actor.is_attacking:
        if actor.anim_state != "attack":
            actor.anim_state = "attack"
            actor.anim_frame = 1
            actor.anim_timer = 0
    elif math.fabs(actor.vx) > 0:
        if actor.vx > 0:
            if actor.anim_state != "walk_right":
                actor.anim_state = "walk_right"
                actor.anim_frame = 1
                actor.anim_timer = 0
        elif actor.vx < 0:
            if actor.anim_state != "walk_left":
                actor.anim_state = "walk_left"
                actor.anim_frame = 1
                actor.anim_timer = 0
    else:
        if actor.anim_state != "idle":
            actor.anim_state = "idle"
            actor.anim_frame = 1
            actor.anim_timer = 0

    # Atualiza o frame da animação
    actor.anim_timer += 1

    if actor.dead:
        if actor.anim_timer >= 7:
            if actor.anim_frame < 3:
                actor.anim_frame += 1
                if actor.anim_frame > total_dead_frames:
                    actor.anim_frame = 1
                actor.image = f"{actor.name}_dead_{actor.anim_frame}"
                actor.anim_timer = 0
    elif actor.anim_state == "idle":
        if actor.anim_timer >= 7:
            actor.anim_frame += 1
            if actor.anim_frame > total_idle_frames:
                actor.anim_frame = 1
            actor.image = f"{actor.name}_idle_{actor.anim_frame}"
            actor.anim_timer = 0
    elif actor.anim_state == "walk_right":
        if actor.anim_timer >= 5:
            actor.anim_frame += 1
            if actor.anim_frame > total_walk_frames:
                actor.anim_frame = 1
            actor.image = f"{actor.name}_walk_right_{actor.anim_frame}"
            actor.anim_timer = 0
    elif actor.anim_state == "walk_left":
        if actor.anim_timer >= 5:
            actor.anim_frame += 1
            if actor.anim_frame > total_walk_frames:
                actor.anim_frame = 1
            actor.image = f"{actor.name}_walk_left_{actor.anim_frame}"
            actor.anim_timer = 0
    elif actor.anim_state == "attack":
        if actor.anim_timer >= 4:  # Ajude de velocidade
            actor.anim_frame += 1
            if actor.anim_frame > total_attack_frames:
                actor.anim_frame = 1
                actor.is_attacking = False  # Finaliza o ataque após a animação
            actor.image = f"{actor.name}_attack_{actor.anim_frame}"
            actor.anim_timer = 0

# Função para detectar colisão com o chão (simples)
def is_on_ground():
    return player.y + player.height//2 >= HEIGHT - 30

# Funções para tocar música do menu
def play_menu_music():
    if not is_muted:
        music.play('menu_music')
        music.set_volume(0.5)

def play_game_music():
    if not is_muted:
        music.play('gameplay_music')
        music.set_volume(0.5)

# Função para desenhar na tela
def draw():
    screen.clear()
    if game_state == "Menu":
        menu_background.draw()
        screen.draw.text("Super Ninja", center=(WIDTH//2, 150), fontsize=80, color="orange", owidth=1, ocolor="white")
        for btn in buttons:
                screen.draw.filled_rect(btn["rect"], "darkblue")
                screen.draw.rect(btn["rect"], "white")
                screen.draw.text(
                    btn["label"] if btn["label"] != "Mute" or not is_muted else "Unmute",
                    center=btn["rect"].center, fontsize=40, color="white"
                )
    elif game_state == "Playing":
        game_background.draw()
        platform.draw()
        player.draw()
        enemy1.draw()
        enemy2.draw()

# Função de eventos do mouse
def on_mouse_down(pos):
    global game_state, is_muted
    if game_state == "Menu":
        for btn in buttons:
            if btn["rect"].collidepoint(pos):
                if btn["action"] == "start":
                    game_state = "Playing"
                    play_game_music()
                elif btn["action"] == "mute":
                    is_muted = not is_muted
                    if is_muted:
                        music.set_volume(0)
                    else:
                        music.set_volume(0.5)
                elif btn["action"] == "quit":
                    exit()

# Eventos de teclas pressionadas
def on_key_down(key):
    global game_state
    if key == keys.ESCAPE and game_state == "Playing":
        game_state = "Menu"
        play_menu_music()
    if key == keys.D:
        player.vx += PLAYER_SPEED
    elif key == keys.A:
        player.vx -= PLAYER_SPEED
    elif key == keys.W and player.on_ground:
        player.vy = -JUMP_STRENGTH
        player.on_ground = False
        if not is_muted and game_state == "Playing":
            sounds.jump.play()
    elif key == keys.SPACE and game_state == "Playing":
        player.is_attacking = True
        if not is_muted:
            sounds.attack.play()

# Evento de teclas soltas
def on_key_up(key):
    if key == keys.D:
        player.vx -= PLAYER_SPEED
    elif key == keys.A:
        player.vx += PLAYER_SPEED
    elif key == keys.SPACE:
        player.is_attacking = False

def update_enemy_position(enemy):
    enemy.x += enemy.vx
    enemy.y += enemy.vy
    
    if enemy.on_rest_delay:
        enemy.current_rest_delay += 1
        if enemy.current_rest_delay >= enemy.rest_delay:
            enemy.on_rest_delay = False
            enemy.current_rest_delay = 0
    else:
        if not enemy.reach_target_1:
            enemy.vx = 1
            if enemy.x >= enemy.x_target_1:
                enemy.vx = 0
                enemy.anim_state = "idle"
                enemy.reach_target_1 = True
                enemy.reach_target_2 = False
                enemy.on_rest_delay = True
        else:
            enemy.vx = -1
            if enemy.x <= enemy.x_target_2:
                enemy.reach_target_2 = True
                enemy.reach_target_1 = False
                enemy.vx = 0
                enemy.anim_state = "idle"
                enemy.on_rest_delay = True

# Atualiza o movimento do jogador
def update():
    if game_state == "Playing":
        # Aplicar gravidade
        player.vy += GRAVITY

        # Atualizar posição do jogador
        player.x += player.vx
        player.y += player.vy

        # Verificar se o jogador está no chão
        if is_on_ground():
            player.on_ground = True
            player.vy = 0
            player.y = HEIGHT - 30 - player.height // 2
        else:
            player.on_ground = False

        # Mantém o jogador dentro dos limites da tela
        if player.left < 0:
            player.left = 0
        if player.right > WIDTH:
            player.right = WIDTH
        
        # Plataforma
        if player.vy > 0 and player.y + player.height // 2 >= platform.y - platform.height // 2:
            if player.x > platform.left and player.x < platform.right:
                player.y = platform.y - player.height // 2 - platform.height // 2
                player.vy = 0
                player.on_ground = True


        for e in [enemy1, enemy2]:
            if not e.dead:
                # Atualiza posição do inimigo
                update_enemy_position(e)
            
        # Detecta colisão entre jogador e inimigo
        for e in [enemy1, enemy2]:
            if player.is_attacking and player.colliderect(e):
                if not e.dead:
                    e.dead = True
                    if not is_muted:
                        sounds.dying.play()

        # Atualiza animação do jogador e dos inimigos
        update_actor_animation(player, 6, 7, 4, 0)
        update_actor_animation(enemy1, 6, 8, 0, 3)
        update_actor_animation(enemy2, 6, 8, 0, 3)

# Iniciar o jogo
play_menu_music()
pgzrun.go()