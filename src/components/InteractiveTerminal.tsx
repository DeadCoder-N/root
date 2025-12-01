import { useState, useEffect, useRef } from 'react';
import { Terminal as TerminalIcon, ChevronRight } from 'lucide-react';

interface Command {
  input: string;
  output: string[];
}

export default function InteractiveTerminal() {
  const [history, setHistory] = useState<Command[]>([]);
  const [currentInput, setCurrentInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const terminalRef = useRef<HTMLDivElement>(null);

  const commands: { [key: string]: string[] } = {
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
      'Email: your.email@example.com',
      'Location: Mumbai, India',
      'GitHub: github.com/yourprofile',
      'LinkedIn: linkedin.com/in/yourprofile',
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

  const processCommand = (input: string): string[] => {
    const cmd = input.trim().toLowerCase();

    if (cmd === 'clear') {
      setHistory([]);
      return [];
    }

    if (commands[cmd]) {
      return commands[cmd];
    }

    if (cmd === '') {
      return [];
    }

    return [`Command not found: ${input}`, 'Type "help" for available commands'];
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentInput.trim() || isTyping) return;

    const output = processCommand(currentInput);

    if (currentInput.trim().toLowerCase() !== 'clear') {
      setHistory([...history, { input: currentInput, output }]);
    }

    setCurrentInput('');
  };

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [history]);

  useEffect(() => {
    const welcomeMessage = {
      input: '',
      output: [
        'Welcome to Nitesh\'s Interactive Terminal!',
        'Type "help" to see available commands.',
        '',
      ],
    };
    setHistory([welcomeMessage]);
  }, []);

  return (
    <section className="py-20 bg-secondary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Interactive <span className="gradient-text">Terminal</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            Try out commands and explore my portfolio in a unique way
          </p>
        </div>

        <div className="max-w-4xl mx-auto fade-in">
          <div className="glass-card overflow-hidden">
            <div className="bg-tertiary px-4 py-3 flex items-center justify-between border-b border-accent-teal/30">
              <div className="flex items-center space-x-2">
                <TerminalIcon className="w-5 h-5 text-accent-teal" />
                <span className="font-mono text-sm">portfolio@terminal:~</span>
              </div>
              <div className="flex space-x-2">
                <div className="w-3 h-3 rounded-full bg-accent-pink"></div>
                <div className="w-3 h-3 rounded-full bg-accent-gold"></div>
                <div className="w-3 h-3 rounded-full bg-accent-green"></div>
              </div>
            </div>

            <div
              ref={terminalRef}
              className="bg-primary p-6 h-96 overflow-y-auto font-mono text-sm"
            >
              {history.map((cmd, index) => (
                <div key={index} className="mb-4">
                  {cmd.input && (
                    <div className="flex items-center space-x-2 text-accent-teal">
                      <ChevronRight className="w-4 h-4" />
                      <span className="text-accent-purple">guest@portfolio</span>
                      <span className="text-text-muted">:</span>
                      <span className="text-accent-teal">~</span>
                      <span className="text-text-muted">$</span>
                      <span className="text-text-primary">{cmd.input}</span>
                    </div>
                  )}
                  {cmd.output.map((line, i) => (
                    <div key={i} className="text-text-secondary ml-6 mt-1">
                      {line}
                    </div>
                  ))}
                </div>
              ))}

              <form onSubmit={handleSubmit} className="flex items-center space-x-2">
                <ChevronRight className="w-4 h-4 text-accent-teal" />
                <span className="text-accent-purple">guest@portfolio</span>
                <span className="text-text-muted">:</span>
                <span className="text-accent-teal">~</span>
                <span className="text-text-muted">$</span>
                <input
                  type="text"
                  value={currentInput}
                  onChange={(e) => setCurrentInput(e.target.value)}
                  className="flex-1 bg-transparent outline-none text-text-primary"
                  placeholder="Type a command..."
                  autoFocus
                />
              </form>
            </div>

            <div className="bg-tertiary px-4 py-2 border-t border-accent-teal/30">
              <p className="text-xs text-text-muted">
                Tip: Try commands like "help", "about", "skills", or even "hack"
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
