import { Github, Linkedin, Mail, Twitter, Shield, Heart } from 'lucide-react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const quickLinks = [
    { label: 'Home', href: '#home' },
    { label: 'About', href: '#about' },
    { label: 'Skills', href: '#skills' },
    { label: 'Projects', href: '#projects' },
  ];

  const resources = [
    { label: 'Blog', href: '#blog' },
    { label: 'Experience', href: '#experience' },
    { label: 'Contact', href: '#contact' },
    { label: 'Resume', href: '/Nitesh_Sawardekar_Resume.pdf' },
  ];

  const socialLinks = [
    { icon: Github, href: 'https://github.com', label: 'GitHub' },
    { icon: Linkedin, href: 'https://linkedin.com', label: 'LinkedIn' },
    { icon: Twitter, href: 'https://twitter.com', label: 'Twitter' },
    { icon: Mail, href: 'mailto:your.email@example.com', label: 'Email' },
  ];

  return (
    <footer className="bg-secondary border-t border-tertiary">
      <div className="container mx-auto px-6 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Shield className="w-8 h-8 text-accent-teal" />
              <span className="text-xl font-bold gradient-text">Dead Coder</span>
            </div>
            <p className="text-text-muted text-sm leading-relaxed">
              Cybersecurity enthusiast and frontend developer passionate about building secure, scalable applications.
            </p>
            <div className="flex space-x-4">
              {socialLinks.map((social, index) => (
                <a
                  key={index}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={social.label}
                  className="text-text-muted hover:text-accent-teal transition-colors transform hover:scale-110"
                >
                  <social.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4 text-accent-teal">Quick Links</h3>
            <ul className="space-y-2">
              {quickLinks.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-text-muted hover:text-accent-teal transition-colors text-sm"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4 text-accent-teal">Resources</h3>
            <ul className="space-y-2">
              {resources.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.href}
                    className="text-text-muted hover:text-accent-teal transition-colors text-sm"
                    {...(link.href.startsWith('http') || link.href.endsWith('.pdf')
                      ? { target: '_blank', rel: 'noopener noreferrer' }
                      : {})}
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4 text-accent-teal">Get In Touch</h3>
            <p className="text-text-muted text-sm mb-4">
              Interested in working together or have a question?
            </p>
            <a href="#contact" className="btn-primary text-sm inline-block">
              Contact Me
            </a>
          </div>
        </div>

        <div className="border-t border-tertiary pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <p className="text-text-muted text-sm text-center md:text-left">
              &copy; {currentYear} Nitesh Sawardekar. All rights reserved.
            </p>
            <p className="text-text-muted text-sm flex items-center space-x-1">
              <span>Built with</span>
              <Heart className="w-4 h-4 text-accent-pink fill-current" />
              <span>using React & TypeScript</span>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
