<!--
INSTRUCTIONS FOR REQUIREMENTS (EARS FORMAT):
- Use EARS format
- Number requirements as REQ-1, REQ-2, etc.
- Keep user stories concise and focused on user value
- Make acceptance criteria specific and testable
- Reference requirements in tasks using: (_Requirements: REQ-1, REQ-3_)

EXAMPLE:
## REQ-1: User Authentication
**User Story:** As a website visitor, I want to create an account so that I can access personalized features.

**Acceptance Criteria:**
- WHEN user provides valid email and password THEN the system SHALL create new account
- WHEN user provides duplicate email THEN the system SHALL show "email already exists" error
- WHEN user provides weak password THEN the system SHALL show password strength requirements

FULL EARS SYNTAX:
While <optional pre-condition>, when <optional trigger>, the <system name> shall <system response>

The EARS ruleset states that a requirement must have: Zero or many preconditions; Zero or one trigger; One system name; One or many system responses.

The application of the EARS notation produces requirements in a small number of patterns, depending on the clauses that are used. The patterns are illustrated below.

Ubiquitous requirements
Ubiquitous requirements are always active (so there is no EARS keyword)

The <system name> shall <system response>

Example: The mobile phone shall have a mass of less than XX grams.

State driven requirements
State driven requirements are active as long as the specified state remains true and are denoted by the keyword While.

While <precondition(s)>, the <system name> shall <system response>

Example: While there is no card in the ATM, the ATM shall display “insert card to begin”.

Event driven requirements
Event driven requirements specify how a system must respond when a triggering event occurs and are denoted by the keyword When.

When <trigger>, the <system name> shall <system response>

Example: When “mute” is selected, the laptop shall suppress all audio output.

Optional feature requirements
Optional feature requirements apply in products or systems that include the specified feature and are denoted by the keyword Where.

Where <feature is included>, the <system name> shall <system response>

Example: Where the car has a sunroof, the car shall have a sunroof control panel on the driver door.

Unwanted behavior requirements
Unwanted behavior requirements are used to specify the required system response to undesired situations and are denoted by the keywords If and Then.

If <trigger>, then the <system name> shall <system response>

Example: If an invalid credit card number is entered, then the website shall display “please re-enter credit card details”.

Complex requirements
The simple building blocks of the EARS patterns described above can be combined to specify requirements for richer system behavior. Requirements that include more than one EARS keyword are called Complex requirements.

While <precondition(s)>, When <trigger>, the <system name> shall <system response>

Example: While the aircraft is on ground, when reverse thrust is commanded, the engine control system shall enable reverse thrust.

Complex requirements for unwanted behavior also include the If-Then keywords.
-->

# CLI UNO Game Requirements

## REQ-1: Classical UNO Gameplay

**User Story:** As a bored meeting attendee, I want to play classical UNO against a computer so that I can be entertained during boring meetings.

**Acceptance Criteria:**

- WHEN the game starts THEN the system SHALL deal 7 cards to player and computer
- WHEN it's player's turn THEN the system SHALL display valid moves and accept card selection
- WHEN a card is played THEN the system SHALL enforce classical UNO rules (color/number matching)
- WHEN special cards are played THEN the system SHALL apply effects (Skip, Reverse, Draw Two, Wild cards)
- WHEN a player has one card left THEN the system SHALL require "UNO!" declaration
- WHEN a player runs out of cards THEN the system SHALL end the round and calculate scores

## REQ-2: Boss Key Feature

**User Story:** As a meeting attendee, I want a boss key to instantly hide the game so that I can avoid detection during meetings.

**Acceptance Criteria:**

- WHEN space bar is pressed THEN the system SHALL immediately clear the screen
- WHEN space bar is pressed THEN the system SHALL display fake terminal output (system commands, logs, etc.)
- WHEN any other key is pressed after boss key THEN the system SHALL return to the game state
- The system SHALL preserve game state during boss key activation
- The fake terminal output SHALL look convincing and work-related

## REQ-3: ASCII Art Interface

**User Story:** As a user, I want visually appealing ASCII art cards so that the game is engaging and fun to play in the terminal.

**Acceptance Criteria:**

- WHEN displaying cards THEN the system SHALL use ASCII art representation
- WHEN showing player hand THEN the system SHALL display cards with clear color and number/symbol indicators
- WHEN displaying the discard pile THEN the system SHALL show the top card prominently
- WHEN showing game state THEN the system SHALL use clear ASCII layouts and borders
- The ASCII art SHALL be readable in standard terminal sizes (80x24 minimum)

## REQ-4: Simple Rule-Based AI Opponent

**User Story:** As a single player, I want to play against a predictable computer opponent so that I can enjoy strategic gameplay without overly complex AI behavior.

**Acceptance Criteria:**

- WHEN it's computer's turn THEN the system SHALL use simple rule-based decision making
- WHEN computer has matching cards THEN the system SHALL prefer color matches over number matches
- WHEN computer has special cards THEN the system SHALL play them strategically (save Wild cards, use Skip/Reverse appropriately)
- WHEN computer has one card THEN the system SHALL automatically declare "UNO!"
- WHEN computer cannot play THEN the system SHALL draw one card and play if possible
- The AI SHALL be challenging but not unbeatable for casual players

## REQ-5: Quick Game Sessions

**User Story:** As a meeting attendee, I want quick game sessions so that I can play during short breaks or boring segments.

**Acceptance Criteria:**

- WHEN the game starts THEN the system SHALL be ready to play within 2 seconds
- WHEN exiting the game THEN the system SHALL quit immediately without confirmation
- WHEN restarting THEN the system SHALL offer quick restart option
- The system SHALL support games lasting 2-10 minutes typically

## REQ-6: Cross-Platform Terminal Support

**User Story:** As a user, I want the game to work on different operating systems so that I can play it on any computer.

**Acceptance Criteria:**

- WHEN running on Windows THEN the system SHALL work in Command Prompt and PowerShell
- WHEN running on macOS THEN the system SHALL work in Terminal app
- WHEN running on Linux THEN the system SHALL work in standard terminal emulators
- The system SHALL handle different terminal sizes gracefully
- The system SHALL use standard Python libraries for maximum compatibility
