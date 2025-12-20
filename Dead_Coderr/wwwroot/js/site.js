// Portfolio JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeHeader();
    initializeTypingEffect();
    initializeScrollAnimations();
    initializeTerminal();
    initializeContactForm();
    initializeSmoothScrolling();
    initializeThemeToggle();
});

// Header functionality
function initializeHeader() {
    const header = document.getElementById('header');
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    // Header scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('bg-secondary/95', 'backdrop-blur-md', 'shadow-lg');
            header.classList.remove('bg-transparent');
        } else {
            header.classList.remove('bg-secondary/95', 'backdrop-blur-md', 'shadow-lg');
            header.classList.add('bg-transparent');
        }
    });

    // Mobile menu toggle
    mobileMenuToggle.addEventListener('click', function() {
        mobileMenu.classList.toggle('hidden');
    });

    // Close mobile menu when clicking nav links
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', function() {
            mobileMenu.classList.add('hidden');
        });
    });
}

// Typing effect for hero section
function initializeTypingEffect() {
    const roles = ['Cybersecurity Enthusiast', 'Frontend Developer', 'Penetration Tester', 'Ethical Hacker'];
    const typingContent = document.getElementById('typing-content');
    let roleIndex = 0;

    function typeRole() {
        const currentRole = roles[roleIndex];
        let currentIndex = 0;
        
        const typingInterval = setInterval(() => {
            if (currentIndex <= currentRole.length) {
                typingContent.textContent = currentRole.slice(0, currentIndex);
                currentIndex++;
            } else {
                clearInterval(typingInterval);
                setTimeout(() => {
                    roleIndex = (roleIndex + 1) % roles.length;
                    typeRole();
                }, 2000);
            }
        }, 100);
    }

    typeRole();
}

// Scroll animations
function initializeScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.fade-in').forEach((el) => observer.observe(el));
}

// Interactive Terminal
function initializeTerminal() {
    const terminalContent = document.getElementById('terminal-content');
    let history = [];
    let currentInput = '';

    const commands = {
        help: [
            'Available commands:',
            '  about       - Learn about me',
            '  skills      - View my technical skills',
            '  projects    - List featured projects',
            '  contact     - Get contact information',
            '  whoami      - Display user info',
            '  clear       - Clear terminal',
            '  hack        - Try the secret command',
        ],
        about: [
            'Nitesh Sawardekar (Dead Coder)',
            'Computer Engineering Student',
            'Cybersecurity Enthusiast | Frontend Developer',
            'Specializing in penetration testing and secure web development',
        ],
        skills: [
            'Cybersecurity: VAPT, Burp Suite, Metasploit, Nessus',
            'Frontend: React, TypeScript, JavaScript, Tailwind CSS',
            'Backend: Node.js, Express, MongoDB, PostgreSQL',
            'Languages: Python, Bash, SQL, PHP',
            'Tools: Git, Docker, Linux, Wireshark',
        ],
        projects: [
            '1. Vulnerability Scanner - Automated web app security testing',
            '2. Secure Chat App - E2E encrypted messaging platform',
            '3. Network Traffic Analyzer - Real-time packet analysis',
            '4. CTF Challenge Platform - Interactive learning environment',
            '5. Password Strength Analyzer - Advanced security checker',
        ],
        contact: [
            'Email: niteshsawardekar972@gmail.com',
            'Phone No: +91 8454806491',
            'Location: Mumbai, India',
            'GitHub: https://github.com/DeadCoder-N',
            'LinkedIn: https://www.linkedin.com/in/nitesh-sawardekar-39708a310/',
        ],
        whoami: ['guest@portfolio-terminal'],
        ls: ['about.txt', 'skills.md', 'projects.json', 'contact.info', 'resume.pdf'],
        pwd: ['/home/nitesh/portfolio'],
        date: [new Date().toString()],
        clear: [],
        hack: [
            'Initializing penetration test...',
            'Scanning ports... [################] 100%',
            'Exploiting vulnerabilities...',
            'Access DENIED: Nice try! This is a portfolio site :)',
            'But I appreciate your curiosity!',
        ],
    };

    function processCommand(input) {
        const cmd = input.trim().toLowerCase();

        if (cmd === 'clear') {
            history = [];
            renderTerminal();
            return;
        }

        if (commands[cmd]) {
            history.push({ input: input, output: commands[cmd] });
        } else if (cmd === '') {
            return;
        } else {
            history.push({ 
                input: input, 
                output: [`Command not found: ${input}`, 'Type "help" for available commands'] 
            });
        }

        renderTerminal();
    }

    function renderTerminal() {
        let content = '';
        
        history.forEach(cmd => {
            if (cmd.input) {
                content += `
                    <div class="mb-4">
                        <div class="flex items-center space-x-2 text-accent-teal">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                            </svg>
                            <span class="text-accent-purple">guest@portfolio</span>
                            <span class="text-text-muted">:</span>
                            <span class="text-accent-teal">~</span>
                            <span class="text-text-muted">$</span>
                            <span class="text-text-primary">${cmd.input}</span>
                        </div>
                        ${cmd.output.map(line => `<div class="text-text-secondary ml-6 mt-1">${line}</div>`).join('')}
                    </div>
                `;
            } else {
                content += `
                    <div class="mb-4">
                        ${cmd.output.map(line => `<div class="text-text-secondary ml-6 mt-1">${line}</div>`).join('')}
                    </div>
                `;
            }
        });

        content += `
            <div class="flex items-center space-x-2">
                <svg class="w-4 h-4 text-accent-teal" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
                <span class="text-accent-purple">guest@portfolio</span>
                <span class="text-text-muted">:</span>
                <span class="text-accent-teal">~</span>
                <span class="text-text-muted">$</span>
                <input type="text" id="terminal-input" class="flex-1 bg-transparent outline-none text-text-primary" placeholder="Type a command..." autofocus>
            </div>
        `;

        terminalContent.innerHTML = content;
        terminalContent.scrollTop = terminalContent.scrollHeight;

        // Add event listener to new input
        const terminalInput = document.getElementById('terminal-input');
        if (terminalInput) {
            terminalInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    processCommand(this.value);
                    this.value = '';
                }
            });
            terminalInput.focus();
        }
    }

    // Initialize terminal with welcome message
    history.push({
        input: '',
        output: [
            "Welcome to Nitesh's Interactive Terminal!",
            'Type "help" to see available commands.',
            '',
        ]
    });
    renderTerminal();
}

// Contact form
function initializeContactForm() {
    const contactForm = document.getElementById('contact-form');
    
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject'),
            message: formData.get('message')
        };

        try {
            const response = await fetch('/Home/Contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.success) {
                alert('Message sent successfully!');
                this.reset();
            } else {
                alert('Error sending message. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error sending message. Please try again.');
        }
    });
}

// Smooth scrolling
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Theme toggle (placeholder - can be extended)
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    
    themeToggle.addEventListener('click', function() {
        // Theme toggle functionality can be implemented here
        console.log('Theme toggle clicked');
    });
}

// Download CV functionality
document.getElementById('download-cv').addEventListener('click', function() {
    // Create a temporary link to download the resume
    const link = document.createElement('a');
    link.href = '/images/Nitesh_Sawardekar_Resume.pdf';
    link.download = 'Nitesh_Sawardekar_Resume.pdf';
    link.click();
    
    // Also open in new tab
    window.open('/images/Nitesh_Sawardekar_Resume.pdf', '_blank');
});

// Add CSS classes for navigation
const style = document.createElement('style');
style.textContent = `
    .nav-link {
        color: var(--text-secondary);
        font-weight: 500;
        position: relative;
        transition: color 0.3s ease;
        text-decoration: none;
        padding-bottom: 4px;
    }
    
    .nav-link:hover {
        color: var(--accent-teal);
        text-decoration: none;
    }
    
    .nav-link::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 0;
        height: 2px;
        background: var(--accent-teal);
        transition: width 0.3s ease;
    }
    
    .nav-link:hover::after {
        width: 100%;
    }
    
    .mobile-nav-link {
        display: block;
        padding: 8px 16px;
        color: var(--text-secondary);
        text-decoration: none;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .mobile-nav-link:hover {
        color: var(--accent-teal);
        background: rgba(45, 55, 72, 0.5);
        text-decoration: none;
    }
    
    @keyframes bounce {
        0%, 20%, 53%, 80%, 100% {
            transform: translate3d(0,0,0);
        }
        40%, 43% {
            transform: translate3d(0,-30px,0);
        }
        70% {
            transform: translate3d(0,-15px,0);
        }
        90% {
            transform: translate3d(0,-4px,0);
        }
    }
    
    .animate-bounce {
        animation: bounce 1s infinite;
    }
    
    .animate-pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: .5;
        }
    }
`;
document.head.appendChild(style);