import { ExternalLink, Github, Shield, Globe, Terminal, Lock } from 'lucide-react';

export default function Projects() {
  const projects = [
    {
      title: 'Vulnerability Scanner',
      category: 'Cybersecurity Tool',
      description: 'Automated web application vulnerability scanner built with Python. Detects SQL injection, XSS, CSRF, and other OWASP Top 10 vulnerabilities.',
      image: 'https://images.pexels.com/photos/1181263/pexels-photo-1181263.jpeg?auto=compress&cs=tinysrgb&w=800',
      technologies: ['Python', 'BeautifulSoup', 'Requests', 'Threading'],
      icon: Shield,
      color: 'from-accent-teal to-cyan-500',
      github: 'https://github.com',
      live: null,
      highlights: ['Scans 50+ vulnerability types', 'Generates detailed reports', 'Multi-threaded scanning'],
    },
    {
      title: 'Secure Chat Application',
      category: 'Full Stack Security',
      description: 'End-to-end encrypted chat application with user authentication, featuring AES-256 encryption and secure key exchange.',
      image: 'https://images.pexels.com/photos/1089438/pexels-photo-1089438.jpeg?auto=compress&cs=tinysrgb&w=800',
      technologies: ['React', 'Node.js', 'Socket.io', 'Crypto-js', 'JWT'],
      icon: Lock,
      color: 'from-accent-purple to-pink-500',
      github: 'https://github.com',
      live: 'https://example.com',
      highlights: ['E2E encryption', 'Real-time messaging', 'Secure authentication'],
    },
    {
      title: 'Network Traffic Analyzer',
      category: 'Security Monitoring',
      description: 'Real-time network traffic monitoring tool that captures and analyzes packets, detects suspicious activities and generates alerts.',
      image: 'https://images.pexels.com/photos/1181675/pexels-photo-1181675.jpeg?auto=compress&cs=tinysrgb&w=800',
      technologies: ['Python', 'Scapy', 'Wireshark', 'Matplotlib'],
      icon: Terminal,
      color: 'from-accent-pink to-red-500',
      github: 'https://github.com',
      live: null,
      highlights: ['Live packet capture', 'Protocol analysis', 'Anomaly detection'],
    },
    {
      title: 'Portfolio Website',
      category: 'Frontend Development',
      description: 'Modern, responsive portfolio website with dark mode, animations, and interactive elements. Built with React and TypeScript.',
      image: 'https://images.pexels.com/photos/196644/pexels-photo-196644.jpeg?auto=compress&cs=tinysrgb&w=800',
      technologies: ['React', 'TypeScript', 'Tailwind CSS', 'Vite'],
      icon: Globe,
      color: 'from-accent-gold to-yellow-500',
      github: 'https://github.com',
      live: 'https://example.com',
      highlights: ['Fully responsive', 'Smooth animations', 'SEO optimized'],
    },
    {
      title: 'Password Strength Analyzer',
      category: 'Security Tool',
      description: 'Advanced password strength checker with entropy calculation, breach detection via HaveIBeenPwned API, and password generation.',
      image: 'https://images.pexels.com/photos/60504/security-protection-anti-virus-software-60504.jpeg?auto=compress&cs=tinysrgb&w=800',
      technologies: ['JavaScript', 'React', 'API Integration', 'Zxcvbn'],
      icon: Shield,
      color: 'from-accent-green to-emerald-500',
      github: 'https://github.com',
      live: 'https://example.com',
      highlights: ['Entropy calculation', 'Breach detection', 'Secure generator'],
    },
    {
      title: 'CTF Challenge Platform',
      category: 'Learning Platform',
      description: 'Interactive platform for practicing cybersecurity skills with various challenges including web, crypto, forensics, and binary exploitation.',
      image: 'https://images.pexels.com/photos/1181467/pexels-photo-1181467.jpeg?auto=compress&cs=tinysrgb&w=800',
      technologies: ['React', 'Node.js', 'MongoDB', 'Docker'],
      icon: Terminal,
      color: 'from-blue-500 to-cyan-500',
      github: 'https://github.com',
      live: 'https://example.com',
      highlights: ['40+ challenges', 'Progress tracking', 'Leaderboard system'],
    },
  ];

  return (
    <section id="projects" className="py-20 bg-primary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Featured <span className="gradient-text">Projects</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            A showcase of my work in cybersecurity and web development
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {projects.map((project, index) => (
            <div
              key={index}
              className="glass-card overflow-hidden group fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="relative h-48 overflow-hidden">
                <img
                  src={project.image}
                  alt={project.title}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-secondary via-secondary/50 to-transparent"></div>
                <div className={`absolute top-4 right-4 w-12 h-12 bg-gradient-to-r ${project.color} rounded-lg flex items-center justify-center`}>
                  <project.icon className="w-6 h-6 text-white" />
                </div>
              </div>

              <div className="p-6 space-y-4">
                <div>
                  <span className="text-xs text-accent-teal font-mono uppercase tracking-wider">
                    {project.category}
                  </span>
                  <h3 className="text-xl font-bold mt-2 group-hover:text-accent-teal transition-colors">
                    {project.title}
                  </h3>
                </div>

                <p className="text-text-muted text-sm leading-relaxed">
                  {project.description}
                </p>

                <div className="space-y-2">
                  <h4 className="text-xs font-semibold text-accent-teal uppercase">Key Features:</h4>
                  <ul className="space-y-1">
                    {project.highlights.map((highlight, i) => (
                      <li key={i} className="text-xs text-text-secondary flex items-start">
                        <span className="text-accent-teal mr-2">▹</span>
                        {highlight}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="flex flex-wrap gap-2">
                  {project.technologies.map((tech, i) => (
                    <span key={i} className="skill-badge text-xs">
                      {tech}
                    </span>
                  ))}
                </div>

                <div className="flex gap-4 pt-4 border-t border-tertiary">
                  {project.github && (
                    <a
                      href={project.github}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center space-x-2 text-text-secondary hover:text-accent-teal transition-colors"
                    >
                      <Github className="w-4 h-4" />
                      <span className="text-sm">Code</span>
                    </a>
                  )}
                  {project.live && (
                    <a
                      href={project.live}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center space-x-2 text-text-secondary hover:text-accent-teal transition-colors"
                    >
                      <ExternalLink className="w-4 h-4" />
                      <span className="text-sm">Live Demo</span>
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center fade-in">
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-secondary inline-flex items-center space-x-2"
          >
            <Github className="w-5 h-5" />
            <span>View All Projects on GitHub</span>
          </a>
        </div>
      </div>
    </section>
  );
}
