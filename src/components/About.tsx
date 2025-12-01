import { Shield, Code, Target, Award } from 'lucide-react';

export default function About() {
  const highlights = [
    {
      icon: Shield,
      title: 'Security First',
      description: 'Experienced in VAPT, ethical hacking, and secure code practices',
    },
    {
      icon: Code,
      title: 'Full Stack Development',
      description: 'Building modern, responsive web applications with latest technologies',
    },
    {
      icon: Target,
      title: 'Problem Solver',
      description: 'Analytical mindset focused on identifying and resolving vulnerabilities',
    },
    {
      icon: Award,
      title: 'Continuous Learner',
      description: 'Always updating skills with latest security trends and frameworks',
    },
  ];

  return (
    <section id="about" className="py-20 bg-secondary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            About <span className="gradient-text">Me</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            Passionate about securing the digital world and creating exceptional user experiences
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6 fade-in">
            <p className="text-text-secondary leading-relaxed">
              I'm a Computer Engineering student with a strong focus on cybersecurity and frontend development.
              My journey in tech has been driven by curiosity about how systems work and how to make them more secure.
            </p>
            <p className="text-text-secondary leading-relaxed">
              I specialize in penetration testing, vulnerability assessments, and building secure web applications.
              My approach combines technical expertise with creative problem-solving to deliver robust solutions.
            </p>
            <p className="text-text-secondary leading-relaxed">
              When I'm not hunting for vulnerabilities or coding, I'm participating in CTF challenges,
              contributing to open-source projects, and sharing my knowledge through technical blogs.
            </p>

            <div className="grid grid-cols-2 gap-4 pt-6">
              <div className="bg-tertiary/50 p-4 rounded-lg border border-accent-teal/30">
                <p className="text-3xl font-bold text-accent-teal">50+</p>
                <p className="text-text-muted text-sm">CTF Challenges</p>
              </div>
              <div className="bg-tertiary/50 p-4 rounded-lg border border-accent-purple/30">
                <p className="text-3xl font-bold text-accent-purple">10+</p>
                <p className="text-text-muted text-sm">Certifications</p>
              </div>
              <div className="bg-tertiary/50 p-4 rounded-lg border border-accent-pink/30">
                <p className="text-3xl font-bold text-accent-pink">5+</p>
                <p className="text-text-muted text-sm">Live Projects</p>
              </div>
              <div className="bg-tertiary/50 p-4 rounded-lg border border-accent-green/30">
                <p className="text-3xl font-bold text-accent-green">3+</p>
                <p className="text-text-muted text-sm">Years Learning</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 fade-in">
            {highlights.map((item, index) => (
              <div
                key={index}
                className="glass-card p-6 space-y-4"
              >
                <div className="w-12 h-12 bg-gradient-to-r from-accent-teal to-accent-purple rounded-lg flex items-center justify-center">
                  <item.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold">{item.title}</h3>
                <p className="text-text-muted text-sm leading-relaxed">
                  {item.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
