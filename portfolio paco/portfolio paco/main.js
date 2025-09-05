// Portfolio JavaScript - Interactive Terminal and Navigation
(function () {
    'use strict';

    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Interactive Terminal
    class InteractiveTerminal {
        constructor() {
            this.terminalBody = document.getElementById('terminal-body');
            this.currentInput = null;
            this.cursor = null;
            this.commandHistory = [];
            this.historyIndex = -1;
            this.currentCommand = '';
            this.activeInputLine = null;
            this.init();
        }

        init() {
            if (!this.terminalBody) return;

            this.setupEventListeners();
            this.setupInitialInput();
        }

        setupEventListeners() {
            // Focus terminal on click
            this.terminalBody.addEventListener('click', () => {
                this.focusTerminal();
            });

            // Keyboard input - listen globally
            document.addEventListener('keydown', (e) => {
                // Only handle if terminal is focused
                if (this.terminalBody === document.activeElement) {
                    e.preventDefault();
                    this.handleKeyPress(e);
                }
            });

            // Mobile touch support
            this.terminalBody.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.focusTerminal();
            });
        }

        setupInitialInput() {
            // Find the initial input line and set it as active
            this.activeInputLine = this.terminalBody.querySelector('.terminal-input-line');
            if (this.activeInputLine) {
                this.currentInput = this.activeInputLine.querySelector('.terminal-text');
            }
            this.focusTerminal();
        }

        focusTerminal() {
            this.terminalBody.focus();
            this.terminalBody.setAttribute('tabindex', '0');
        }

        handleKeyPress(e) {
            const key = e.key;

            if (key === 'Enter') {
                e.preventDefault();
                this.executeCommand();
            } else if (key === 'Backspace') {
                this.handleBackspace();
            } else if (key === 'ArrowUp') {
                this.navigateHistory(-1);
            } else if (key === 'ArrowDown') {
                this.navigateHistory(1);
            } else if (key === 'Tab') {
                e.preventDefault();
                this.handleTabCompletion();
            } else if (key.length === 1 && !e.ctrlKey && !e.metaKey) {
                this.addCharacter(key);
            }
        }

        addCharacter(char) {
            this.currentCommand += char;
            this.updateInputDisplay();
        }

        handleBackspace() {
            if (this.currentCommand.length > 0) {
                this.currentCommand = this.currentCommand.slice(0, -1);
                this.updateInputDisplay();
            }
        }

        updateInputDisplay() {
            if (this.currentInput) {
                // Limpiar el contenido anterior
                this.currentInput.innerHTML = '';

                // Crear span para el texto
                const textSpan = document.createElement('span');
                textSpan.textContent = this.currentCommand;
                this.currentInput.appendChild(textSpan);

                // Crear span para el cursor
                const cursorSpan = document.createElement('span');
                cursorSpan.className = 'terminal-cursor';
                cursorSpan.textContent = '_';
                this.currentInput.appendChild(cursorSpan);
            }
        }

        navigateHistory(direction) {
            if (this.commandHistory.length === 0) return;

            this.historyIndex += direction;

            if (this.historyIndex < 0) {
                this.historyIndex = -1;
                this.currentCommand = '';
            } else if (this.historyIndex >= this.commandHistory.length) {
                this.historyIndex = this.commandHistory.length - 1;
            }

            if (this.historyIndex >= 0) {
                this.currentCommand = this.commandHistory[this.historyIndex];
            }

            this.updateInputDisplay();
        }

        handleTabCompletion() {
            const commands = Object.keys(this.getCommands());
            const matches = commands.filter(cmd => cmd.startsWith(this.currentCommand));

            if (matches.length === 1) {
                this.currentCommand = matches[0];
                this.updateInputDisplay();
            } else if (matches.length > 1) {
                this.showOutput(matches.join(' '));
            }
        }

        executeCommand() {
            const command = this.currentCommand.trim();

            if (command) {
                this.addToHistory(command);
                this.lockCurrentInputLine(command);
                this.processCommand(command);
                this.createNewInputLine();
            }

            this.currentCommand = '';
        }

        addToHistory(command) {
            if (command && this.commandHistory[this.commandHistory.length - 1] !== command) {
                this.commandHistory.push(command);
                if (this.commandHistory.length > 50) {
                    this.commandHistory.shift();
                }
            }
            this.historyIndex = this.commandHistory.length;
        }

        lockCurrentInputLine(command) {
            if (this.activeInputLine) {
                // Lock the current input line by making it read-only
                const commandSpan = this.activeInputLine.querySelector('.terminal-text');
                if (commandSpan) {
                    commandSpan.textContent = command;
                    commandSpan.className = 'terminal-command';
                }

                // Remove input line class to make it read-only
                this.activeInputLine.classList.remove('terminal-input-line');
                this.activeInputLine = null;
                this.currentInput = null;
            }
        }

        processCommand(command) {
            const commands = this.getCommands();
            const output = commands[command] || this.getUnknownCommandOutput(command);

            this.showOutput(output);
        }

        getCommands() {
            return {
                'help': [
                    'Available commands:',
                    '  help           -> Show this list of commands',
                    '  about          -> Who I am in 3 lines',
                    '  skills         -> Tech stack overview',
                    '  projects       -> Highlighted projects with short summaries',
                    '  tfg            -> Final Degree Project (featured)',
                    '  experience     -> Work experience snapshot',
                    '  education      -> Studies and relevant courses',
                    '  certs          -> Certifications',
                    '  vision         -> What I value when building software',
                    '  contact        -> How to reach me',
                    '  clear          -> Clear the terminal'
                ],
                'about': [
                    'Francisco Moya — Full-Stack mindset with a strong back-end focus in Java & Spring Boot.',
                    'I build REST APIs, integrate Bootstrap/Ajax front-ends, and deploy reliably on Linux Ubuntu.',
                    'I care about clean code, security-minded practices, and maintainable systems.'
                ],
                'skills': [
                    'Back-end: Java, Spring Boot, REST APIs, Maven',
                    'Front-end: JavaScript, HTML, CSS, Bootstrap, Ajax',
                    'Databases: SQL Server, MySQL, SQLite, MongoDB',
                    'Testing & QA: JUnit (unit & integration)',
                    'Tools & Agile: Git/GitHub, Scrum/Jira',
                    'OS: Linux Ubuntu, Windows'
                ],
                'projects': [
                    '• REST API CRUD — Java + Spring Boot + SQL; validation & pagination; Postman collection.',
                    '• Bootstrap + Ajax Client — responsive UI consuming the API; forms & dynamic tables.',
                    '• Business Reporting (JasperReports) — PDF reports with date/category filters.',
                    '• Final Degree Project — interactive football mini-games system with Python/customtkinter + MySQL DB.'

                ],
                'tfg': [
                    'Final Degree Project — interactive system of football mini-games connected to a LaLiga database.',
                    'Back-end: Python (data management + MySQL queries).',
                    'Front-end: Python with customtkinter (modern UI for mini-games).',
                    'Results: Validated with LaLiga players/teams data; deployed locally; versioned on GitHub.',
                    'Stack: Python · customtkinter · MySQL · GitHub'

                ],
                'experience': [
                    '2025 — IT Intern @ SICE (Madrid)',
                    '  • Built and maintained internal tools.',
                    '  • Daily deployments & configuration on Linux Ubuntu.',
                    '  • Collaborated under Scrum with senior developers.',
                    '',
                    'Other: 5★ hospitality (Dromoland Castle, Ireland) — customer-facing teamwork and communication.'
                ],
                'education': [
                    'Higher National Diploma — Multiplatform Applications Development (DAM), 2023–2025.',
                    'Relevant: Java, Databases, Web Development, Testing, Agile practices.'
                ],
                'certs': [
                    'Advanced Cybersecurity in Operational Technology Environments — MainJobs, 120h, 2025.'
                ],
                'vision': [
                    'Code should be reliable, secure, and maintainable.',
                    'I value automation, readable architecture, and continuous learning.'
                ],
                'contact': [
                    'Email: pmoyapardo22@gmail.com',
                    'Location: Ennis, Ireland',
                    'GitHub / LinkedIn: available in the navbar'
                ],
                'clear': []
            };
        }

        getUnknownCommandOutput(command) {
            return [
                `Command not found: ${command}`,
                "Type 'help' to see available commands."
            ];
        }

        showOutput(output) {
            if (output.length === 0) {
                this.clearTerminal();
                return;
            }

            const outputDiv = document.createElement('div');
            outputDiv.className = 'terminal-output';

            output.forEach(line => {
                const lineDiv = document.createElement('div');
                lineDiv.className = 'terminal-line';
                const textSpan = document.createElement('span');
                textSpan.className = 'terminal-text';
                textSpan.textContent = line;
                lineDiv.appendChild(textSpan);
                outputDiv.appendChild(lineDiv);
            });

            this.terminalBody.appendChild(outputDiv);
            this.scrollToBottom();
        }

        createNewInputLine() {
            const newLine = document.createElement('div');
            newLine.className = 'terminal-line terminal-input-line';
            newLine.innerHTML = `
                <span class="terminal-prompt">franciscomp@portfolio:~$</span>
                <span class="terminal-text"></span>
            `;

            this.terminalBody.appendChild(newLine);

            // Update references to the new active input line
            this.activeInputLine = newLine;
            this.currentInput = newLine.querySelector('.terminal-text');

            // Ensure terminal stays focused and scrolls to bottom
            this.focusTerminal();
            this.scrollToBottom();
        }

        clearTerminal() {
            // Clear all content except the initial messages
            const allLines = this.terminalBody.querySelectorAll('.terminal-line');
            allLines.forEach((line, index) => {
                if (index > 1) line.remove(); // Keep only the first two lines (initial messages)
            });

            // Clear any output divs
            const outputs = this.terminalBody.querySelectorAll('.terminal-output');
            outputs.forEach(output => output.remove());

            // Reset active input references
            this.activeInputLine = null;
            this.currentInput = null;

            // Create a fresh input line
            this.createNewInputLine();
        }

        scrollToBottom() {
            this.terminalBody.scrollTop = this.terminalBody.scrollHeight;
        }
    }

    // Smooth Scrolling Navigation
    class SmoothScrolling {
        constructor() {
            this.init();
        }

        init() {
            const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');

            navLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const targetId = link.getAttribute('href');
                    const targetElement = document.querySelector(targetId);

                    if (targetElement) {
                        this.scrollToElement(targetElement);
                    }
                });
            });
        }

        scrollToElement(element) {
            const headerHeight = document.querySelector('.header').offsetHeight;
            const elementPosition = element.offsetTop - headerHeight - 20;

            if (prefersReducedMotion) {
                window.scrollTo(0, elementPosition);
            } else {
                window.scrollTo({
                    top: elementPosition,
                    behavior: 'smooth'
                });
            }
        }
    }

    // Active Navigation Highlighting
    class ActiveNavigation {
        constructor() {
            this.sections = document.querySelectorAll('section[id]');
            this.navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
            this.init();
        }

        init() {
            if (this.sections.length === 0 || this.navLinks.length === 0) return;

            window.addEventListener('scroll', this.throttle(this.updateActiveNav.bind(this), 100));
            this.updateActiveNav(); // Initial call
        }

        updateActiveNav() {
            const scrollPosition = window.scrollY + 100;

            this.sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.offsetHeight;
                const sectionId = section.getAttribute('id');

                if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                    this.setActiveNavLink(sectionId);
                }
            });
        }

        setActiveNavLink(activeId) {
            this.navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${activeId}`) {
                    link.classList.add('active');
                }
            });
        }

        throttle(func, limit) {
            let inThrottle;
            return function () {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        }
    }

    // Header Scroll Effect
    class HeaderScrollEffect {
        constructor() {
            this.header = document.querySelector('.header');
            this.init();
        }

        init() {
            if (!this.header) return;

            window.addEventListener('scroll', this.throttle(this.handleScroll.bind(this), 10));
        }

        handleScroll() {
            const scrollY = window.scrollY;

            if (scrollY > 50) {
                this.header.classList.add('scrolled');
            } else {
                this.header.classList.remove('scrolled');
            }
        }

        throttle(func, limit) {
            let inThrottle;
            return function () {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        }
    }

    // Intersection Observer for Animations
    class ScrollAnimations {
        constructor() {
            this.init();
        }

        init() {
            if (prefersReducedMotion) return;

            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-in');
                    }
                });
            }, observerOptions);

            // Observe sections for animation
            const sections = document.querySelectorAll('.section');
            sections.forEach(section => {
                section.classList.add('animate-on-scroll');
                observer.observe(section);
            });
        }
    }

    // Initialize everything when DOM is loaded
    document.addEventListener('DOMContentLoaded', () => {
        new InteractiveTerminal();
        new SmoothScrolling();
        new ActiveNavigation();
        new HeaderScrollEffect();
        new ScrollAnimations();
    });

    // Add CSS for active navigation state
    const style = document.createElement('style');
    style.textContent = `
        .nav-menu a.active {
            color: var(--text-primary) !important;
        }
        
        .nav-menu a.active::after {
            width: 100% !important;
        }
        
        .header.scrolled {
            background: rgba(10, 25, 47, 0.98);
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
        }
        
        .animate-on-scroll {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .animate-on-scroll.animate-in {
            opacity: 1;
            transform: translateY(0);
        }
        
        @media (prefers-reduced-motion: reduce) {
            .animate-on-scroll {
                opacity: 1;
                transform: none;
                transition: none;
            }
        }
    `;
    document.head.appendChild(style);

})();