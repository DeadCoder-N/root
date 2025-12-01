import { Briefcase, GraduationCap, Award } from 'lucide-react';

export default function Experience() {
  const experiences = [
    {
      type: 'work',
      icon: Briefcase,
      title: 'Cybersecurity Intern',
      company: 'Tech Security Solutions',
      period: 'Jun 2024 - Present',
      description: 'Conducting vulnerability assessments, penetration testing on web applications, and assisting in security audit reports.',
      achievements: [
        'Identified 50+ security vulnerabilities across client applications',
        'Developed automated security testing scripts using Python',
        'Contributed to incident response and threat analysis',
      ],
      skills: ['VAPT', 'Burp Suite', 'Python', 'Security Auditing'],
    },
    {
      type: 'work',
      icon: Briefcase,
      title: 'Frontend Developer Intern',
      company: 'Digital Innovations Ltd',
      period: 'Jan 2024 - May 2024',
      description: 'Built responsive web applications and implemented secure authentication systems.',
      achievements: [
        'Developed 5+ client projects using React and TypeScript',
        'Improved application performance by 40%',
        'Implemented secure JWT-based authentication',
      ],
      skills: ['React', 'TypeScript', 'Tailwind CSS', 'REST APIs'],
    },
    {
      type: 'education',
      icon: GraduationCap,
      title: 'Bachelor of Engineering',
      company: 'Computer Engineering',
      period: '2021 - 2025',
      description: 'Specialized in Cybersecurity and Software Development with consistent academic excellence.',
      achievements: [
        'CGPA: 8.5/10',
        'Led Cybersecurity Club and organized workshops',
        'Published research paper on web application security',
      ],
      skills: ['Network Security', 'Algorithm Design', 'Database Systems'],
    },
    {
      type: 'achievement',
      icon: Award,
      title: 'CTF & Bug Bounty',
      company: 'Freelance Security Researcher',
      period: '2023 - Present',
      description: 'Active participation in CTF competitions and bug bounty programs.',
      achievements: [
        'Ranked Top 5% on TryHackMe platform',
        'Solved 100+ CTF challenges across various platforms',
        'Discovered and reported 10+ vulnerabilities through bug bounty',
      ],
      skills: ['Ethical Hacking', 'Web Security', 'Cryptography', 'Forensics'],
    },
  ];

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'work':
        return 'from-accent-teal to-cyan-500';
      case 'education':
        return 'from-accent-purple to-pink-500';
      case 'achievement':
        return 'from-accent-gold to-yellow-500';
      default:
        return 'from-accent-teal to-accent-purple';
    }
  };

  return (
    <section id="experience" className="py-20 bg-secondary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Experience & <span className="gradient-text">Education</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            My professional journey and academic achievements
          </p>
        </div>

        <div className="relative">
          <div className="absolute left-0 md:left-1/2 transform md:-translate-x-1/2 h-full w-0.5 bg-gradient-to-b from-accent-teal via-accent-purple to-accent-pink"></div>

          <div className="space-y-12">
            {experiences.map((exp, index) => (
              <div
                key={index}
                className={`relative flex items-center ${
                  index % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'
                } fade-in`}
              >
                <div className="absolute left-0 md:left-1/2 transform md:-translate-x-1/2 timeline-dot"></div>

                <div className={`w-full md:w-1/2 ${index % 2 === 0 ? 'md:pr-12' : 'md:pl-12'} pl-12 md:pl-0`}>
                  <div className="glass-card p-6 space-y-4">
                    <div className="flex items-start justify-between">
                      <div className={`w-12 h-12 bg-gradient-to-r ${getTypeColor(exp.type)} rounded-lg flex items-center justify-center flex-shrink-0`}>
                        <exp.icon className="w-6 h-6 text-white" />
                      </div>
                      <span className="text-sm text-accent-teal font-mono">{exp.period}</span>
                    </div>

                    <div>
                      <h3 className="text-2xl font-bold mb-1">{exp.title}</h3>
                      <p className="text-accent-purple font-medium">{exp.company}</p>
                    </div>

                    <p className="text-text-muted leading-relaxed">{exp.description}</p>

                    <div className="space-y-2">
                      <h4 className="text-sm font-semibold text-accent-teal">Key Achievements:</h4>
                      <ul className="space-y-1">
                        {exp.achievements.map((achievement, i) => (
                          <li key={i} className="text-sm text-text-secondary flex items-start">
                            <span className="text-accent-teal mr-2">▹</span>
                            {achievement}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="flex flex-wrap gap-2 pt-2">
                      {exp.skills.map((skill, i) => (
                        <span key={i} className="skill-badge text-xs">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
