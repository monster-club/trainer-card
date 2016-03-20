# Trainer Card
[![GitHub tag](https://img.shields.io/github/tag/pokemon-club/trainer-card.svg?style=flat-square)]()
[![Waffle.io](https://img.shields.io/badge/waffle-board-78cbfd.svg?style=flat-square)](https://waffle.io/pokemon-club/admin)
[![Codacy](https://img.shields.io/codacy/1dd32d9e861047909d46c002116038d0.svg?style=flat-square)](https://www.codacy.com/app/scarecrow3322/trainer-card/dashboard)
[![Requires.io](https://img.shields.io/requires/github/pokemon-club/trainer-card.svg?style=flat-square)](https://requires.io/github/pokemon-club/trainer-card/requirements/?branch=master)

Get into the game

![trainer card](http://pokecharms.com/data/trainercardmaker/card/card.png?20111202)

### What is Trainer Card?

Trainer Card is a user account microservice for Pokemon Club. It allows developers to administer user accounts in Pokemon Club, by generating sign-up tokens. It also tracks some meta-data about users, like their current amount of money, score, stars, etc.

Trainer Card currently handles the following:
 1. Creating sign-up tokens
   - Pokemon Club is a private, invitation only service. This allows developers to manage who is allowed to join
 2. Allow people given tokens to sign up
 3. Log in users who have accounts
 4. Update user meta-data

Note: Trainer Card is in beta.
