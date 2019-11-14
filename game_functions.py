import sys
from time import sleep
import random
import math
import pygame
from bullet import Bullet
from alien import Alien
from barrier import Barrier
from smoke import Smoke


def check_keydown_events(event, ai_settings, screen, sounds, ship, bullets, bullet_delay):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, sounds, ship, bullets, bullet_delay)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, sounds, stats, sb, highscores, play_button, high_score_button,
                 ship, aliens, ufo, bullets, bullet_delay, barriers, alien_bullets, smokes, inputs=None):
    pygame.event.pump()
    if inputs is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, ai_settings, screen, sounds, ship, bullets, bullet_delay)

            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not stats.game_active:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if play_button.press(mouse_x, mouse_y):
                        press_play_button(ai_settings, screen, sounds, stats, sb, play_button, ship,
                                          aliens, ufo, bullets, barriers, alien_bullets, smokes, mouse_x, mouse_y)
                    elif high_score_button.press(mouse_x, mouse_y):
                        press_high_score_button(ai_settings, screen, highscores)

    elif len(inputs) == 3:
        if inputs[0] == 1:
            ship.moving_right = True
        else:
            ship.moving_right = False
        if inputs[1] == 1:
            ship.moving_left = True
        else:
            ship.moving_left = False
        if inputs[2] == 1:
            fire_bullet(ai_settings, screen, sounds, ship, bullets, bullet_delay)


def press_high_score_button(ai_settings, screen, highscores):
    screen.fill(ai_settings.bg_color)
    posy = 200
    font = pygame.font.SysFont(None, 48)
    header_img = font.render("High Scores", True, (255, 255, 255))
    header_rect = header_img.get_rect()
    header_rect.top = 150
    header_rect.centerx = 600
    screen.blit(header_img, header_rect)
    for entry in highscores.hs_list:
        posx = 500
        for item in entry:
            highscore_image = font.render(item, True, (255, 255, 255))
            highscore_rect = highscore_image.get_rect()
            highscore_rect.top = posy
            highscore_rect.right = posx
            screen.blit(highscore_image, highscore_rect)
            posx += 300
        posy += 50
    pygame.display.flip()
    sleep(3)


def restart(ai_settings, screen, sounds, stats, sb,
                      ship, aliens, ufo, bullets, barriers, alien_bullets, smokes):
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    aliens.empty()
    bullets.empty()
    alien_bullets.empty()
    barriers.empty()
    smokes.empty()
    ufo.reset()

    sounds.ufo_stop()
    create_fleet(ai_settings, screen, sounds, aliens)
    ship.center_ship()
    create_barriers(ai_settings, screen, barriers)


def press_play_button(ai_settings, screen, sounds, stats, sb,
                      play_button, ship, aliens, ufo, bullets, barriers, alien_bullets, smokes, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        restart(ai_settings, screen, sounds, stats, sb,
                      ship, aliens, ufo, bullets, barriers, alien_bullets, smokes)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, ufo, bullets,
                  menu_bg, play_button, high_score_button, barriers, alien_bullets, smokes, simplify=False):
    if stats.game_active:
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        aliens.draw(screen)
        ufo.blitme()
        barriers.draw(screen)
        alien_bullets.draw(screen)
        if not simplify:
            smokes.draw(screen)

        for bullet in bullets.sprites():
            bullet.blitme()

        if not simplify:
            sb.show_score()

    if not stats.game_active:
        menu_screen(menu_bg, play_button, high_score_button)


def update_bullets(ai_settings, screen, sounds, stats, sb, ship, aliens, ufo,
                   bullets, bullet_delay, barriers, alien_bullets, smokes, alien_timer, ufo_timer, smoke_timer, simplify=False):
    bullets.update(simplify)
    alien_bullets.update(simplify)

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.rect.top >= ai_settings.screen_height:
            alien_bullets.remove(alien_bullet)

    check_bullet_alien_collisions(ai_settings, screen, sounds, stats, sb, ship, aliens, ufo,
                                  bullets, barriers, alien_bullets, smokes, alien_timer, ufo_timer, smoke_timer)
    check_bullet_ufo_collision(ai_settings, screen, stats, sb, ufo, bullets, smokes)
    check_bullet_barrier_collisions(bullets, barriers, alien_bullets)
    check_bullet_ship_collisions(ship, alien_bullets)

def check_bullet_ship_collisions(ship, alien_bullets):
    collision = False
    for bullet in alien_bullets:
        if pygame.sprite.collide_mask(ship, bullet):
            collision = True
    if collision:
        ship.destroy()


def check_bullet_ufo_collision(ai_settings, screen, stats, sb, ufo, bullets, smokes):
    if pygame.sprite.spritecollide(ufo, bullets, True):
        new_smoke = Smoke(ai_settings, screen, 3, ufo.rect.copy())
        smokes.add(new_smoke)
        stats.score += ufo.get_score()
        sb.prep_score()
        check_high_score(stats, sb)
        ufo.destroy()


def check_bullet_alien_collisions(ai_settings, screen, sounds, stats, sb, ship, aliens, ufo,
                                  bullets, barriers, alien_bullets, smokes, alien_timer, ufo_timer, smoke_timer):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)

    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                new_smoke = Smoke(ai_settings, screen, alien.type, alien.rect)
                smokes.add(new_smoke)
                alien.hit()
                # increases speed of aliens the fewer of them there are
                stats.score += alien.get_score()
                sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        alien_timer.reset()
        ufo_timer.reset()
        smoke_timer.reset()
        aliens.empty()
        ship.center_ship()
        bullets.empty()
        alien_bullets.empty()
        barriers.empty()
        smokes.empty()
        ufo.reset()

        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, sounds, aliens)
        create_barriers(ai_settings, screen, barriers)


def check_bullet_barrier_collisions(bullets, barriers, alien_bullets):
    # check for collisions between barriers and both alien and bullet collision
    player_bullet_collisions = pygame.sprite.groupcollide(bullets, barriers, True, False)
    alien_bullet_collisions = pygame.sprite.groupcollide(alien_bullets, barriers, True, False)

    if player_bullet_collisions:
        for barriers in player_bullet_collisions.values():
            for barrier in barriers:
                barrier.damage()

    if alien_bullet_collisions:
        for barriers in alien_bullet_collisions.values():
            for barrier in barriers:
                barrier.damage()


def fire_bullet(ai_settings, screen, sounds, ship, bullets, bullet_delay):
    if len(bullets) < ai_settings.bullets_allowed and bullet_delay <= 0:
        new_bullet = Bullet(ai_settings, screen, ship, True)
        bullets.add(new_bullet)
        sounds.laser_play()



def create_alien(ai_settings, screen, sounds, aliens, alien_number, row_number, alien_type, alt_frame):
    alien = Alien(ai_settings, screen, sounds, alien_type, alt_frame)
    alien.x = \
        ai_settings.alien_start_pos_x + (ai_settings.alien_width - alien.rect.width) / 2 + \
        (ai_settings.alien_width + ai_settings.alien_space_factor) * alien_number
    alien.rect.top = ai_settings.alien_start_pos_y + (row_number
                                                      * (ai_settings.alien_height + ai_settings.alien_space_factor))
    alien.save_spawn()
    aliens.add(alien)


def create_fleet(ai_settings, screen, sounds, aliens):
    alt_frame = False
    for row_number in range(ai_settings.alien_fleet_rows):
        for alien_number in range(ai_settings.alien_fleet_cols):
            create_alien(ai_settings, screen, sounds, aliens, alien_number,
                         row_number, int(math.floor(math.sqrt(2 * (row_number + 1)) + 1/2) + 2) % 3, alt_frame)
#            alt_frame = not alt_frame


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_alien_barrier_collision(aliens, barriers):
    pygame.sprite.groupcollide(barriers, aliens, True, False)


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(stats, sb, highscores, ship, aliens, ufo, bullets, alien_bullets, alien_timer):
    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()
        bullets.empty()
        alien_bullets.empty()
        ship.center_ship()
        for alien in aliens:
            alien.respawn()
        sleep(1)
    else:
        alien_timer.reset()
        ufo.reset()
        highscores.check_place(int(round(stats.score, -1)))
        highscores.hs_print()
        sleep(1)
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(screen, ship, aliens):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship.destroy()
            break


def alien_attack(ai_settings, screen, aliens, alien_bullets):
    alien_count = len(aliens)
    attacker_id = random.randrange(alien_count)
    attacker_count = 0
    for alien in aliens:
        if attacker_count == attacker_id:
            new_alien_bullet = Bullet(ai_settings, screen, alien, False)
            alien_bullets.add(new_alien_bullet)
            break
        attacker_count += 1


def update_aliens(ai_settings, screen, sounds, ship, aliens, barriers, alien_bullets, alien_timer, simplify=False):
    if len(aliens) > 0:
        check_fleet_edges(ai_settings, aliens)
        aliens.update()

        # animate all live aliens with each tick
        if alien_timer.check():
            if not simplify:
                for alien in aliens:
                    alien.rotate()
            alien_attack(ai_settings, screen, aliens, alien_bullets)
            sounds.move_play()
            # decreases the refresh rate based on how many aliens are remaining, speeds up alien animations and firerate
            # max speed is 2x faster than the default
            alien_timer.update(int((alien_timer.default * 1.0 / 2.0)
                                   + ((1.0 / 2.0 * alien_timer.default)
                                      * (float(len(aliens)) / float(ai_settings.alien_fleet_cols * ai_settings.alien_fleet_rows)))))

        # checks if any aliens have have collided with the ship
        if pygame.sprite.spritecollideany(ship, aliens):
            ship.hit = True

        # checks if any aliens have reached the bottom of the screen
        check_aliens_bottom(screen, ship, aliens)

        # checks if any aliens have collided with a barrier to destroy that barrier
        check_alien_barrier_collision(aliens, barriers)


def update_smokes(smokes, smoke_timer):
    if smoke_timer.check():
        for smoke in smokes:
            smoke.rotate()


def update_ufo(ufo, ufo_timer, simplify=False):
    # if ufo has already been destroyed in this level return
    if ufo.hit is True:
        return

    # if timer reaches its cycle and ufo is not on screen
    elif ufo_timer.check() and ufo.active() is False:
        # 25% chance to spawn a UFO every ufo_timer tick if one does not already exist
        if random.randrange(1, 4) == 1:
            # 50% chance to have UFO spawn on left or right
            is_left = random.choice([True, False])
            # sets state for appropriate ufo behavior
            ufo.set_spawn(is_left)

    # if ufo is in active state update ufo
    elif ufo.active():
        ufo.update(simplify)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def create_barriers(ai_settings, screen, barriers):
    saved_x = 265

    for barrier_count in range(ai_settings.barrier_total):
        pos_y = ai_settings.barrier_topy
        barrier_type = 0
        for y in range(ai_settings.barrier_count_y):
            pos_x = saved_x
            for x in range(ai_settings.barrier_count_x):
                new_barrier = Barrier(ai_settings, screen, barrier_type, pos_x, pos_y)
                barriers.add(new_barrier)
                barrier_type += 1
                pos_x += ai_settings.barrier_width
            pos_y += ai_settings.barrier_height
        saved_x += 300


def update_ship(stats, sb, highscores, ship, aliens, ufo, bullets, alien_bullets, ship_timer, alien_timer, simplify=False):
    if not ship.hit:
        ship.update()
    else:
        if ship_timer.check() and not simplify:
            if ship.play_death():
                ship_hit(stats, sb, highscores, ship, aliens, ufo, bullets, alien_bullets, alien_timer)
        else:
            ship_hit(stats, sb, highscores, ship, aliens, ufo, bullets, alien_bullets, alien_timer)


def menu_screen(menu_bg, play_button, high_score_button):
    menu_bg.draw_button()
    play_button.draw_button()
    high_score_button.draw_button()


def update_timers(alien_timer, ufo_timer, ship_timer, smoke_timer):
    alien_timer.tick()
    ufo_timer.tick()
    ship_timer.tick()
    smoke_timer.tick()
