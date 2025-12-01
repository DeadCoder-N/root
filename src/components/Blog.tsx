import { Calendar, Clock, ArrowRight, Tag } from 'lucide-react';

export default function Blog() {
  const blogPosts = [
    {
      title: 'Understanding SQL Injection: A Comprehensive Guide',
      excerpt: 'Deep dive into SQL injection vulnerabilities, how they work, and effective prevention techniques with real-world examples.',
      date: '2024-11-15',
      readTime: '8 min read',
      category: 'Web Security',
      tags: ['SQL Injection', 'OWASP', 'Web Security'],
      image: 'https://images.pexels.com/photos/270348/pexels-photo-270348.jpeg?auto=compress&cs=tinysrgb&w=800',
    },
    {
      title: 'Building Secure React Applications',
      excerpt: 'Best practices for securing React applications including XSS prevention, secure authentication, and protecting sensitive data.',
      date: '2024-11-08',
      readTime: '10 min read',
      category: 'Frontend Security',
      tags: ['React', 'Security', 'XSS'],
      image: 'https://images.pexels.com/photos/11035471/pexels-photo-11035471.jpeg?auto=compress&cs=tinysrgb&w=800',
    },
    {
      title: 'My Journey to Top 5% on TryHackMe',
      excerpt: 'Sharing my strategies, favorite rooms, and tips for aspiring ethical hackers to excel on TryHackMe platform.',
      date: '2024-10-28',
      readTime: '6 min read',
      category: 'Learning',
      tags: ['CTF', 'TryHackMe', 'Career'],
      image: 'https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg?auto=compress&cs=tinysrgb&w=800',
    },
    {
      title: 'Automated Vulnerability Scanning with Python',
      excerpt: 'Learn how to build your own vulnerability scanner using Python, BeautifulSoup, and Requests library.',
      date: '2024-10-20',
      readTime: '12 min read',
      category: 'Tools',
      tags: ['Python', 'Automation', 'VAPT'],
      image: 'https://images.pexels.com/photos/1181271/pexels-photo-1181271.jpeg?auto=compress&cs=tinysrgb&w=800',
    },
    {
      title: 'Network Security Fundamentals',
      excerpt: 'Essential concepts every cybersecurity professional should know about network protocols, firewalls, and intrusion detection.',
      date: '2024-10-10',
      readTime: '7 min read',
      category: 'Network Security',
      tags: ['Networking', 'Firewall', 'IDS/IPS'],
      image: 'https://images.pexels.com/photos/1148820/pexels-photo-1148820.jpeg?auto=compress&cs=tinysrgb&w=800',
    },
    {
      title: 'Mastering Burp Suite for Web Penetration Testing',
      excerpt: 'Complete guide to using Burp Suite effectively for finding and exploiting web application vulnerabilities.',
      date: '2024-09-25',
      readTime: '15 min read',
      category: 'Tools',
      tags: ['Burp Suite', 'Penetration Testing', 'Web Security'],
      image: 'https://images.pexels.com/photos/1181316/pexels-photo-1181316.jpeg?auto=compress&cs=tinysrgb&w=800',
    },
  ];

  const getCategoryColor = (category: string) => {
    const colors: { [key: string]: string } = {
      'Web Security': 'from-accent-teal to-cyan-500',
      'Frontend Security': 'from-accent-purple to-pink-500',
      'Learning': 'from-accent-gold to-yellow-500',
      'Tools': 'from-accent-green to-emerald-500',
      'Network Security': 'from-blue-500 to-cyan-500',
    };
    return colors[category] || 'from-accent-teal to-accent-purple';
  };

  return (
    <section id="blog" className="py-20 bg-secondary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Blog & <span className="gradient-text">Articles</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            Sharing knowledge and insights about cybersecurity and development
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {blogPosts.map((post, index) => (
            <article
              key={index}
              className="glass-card overflow-hidden group cursor-pointer fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="relative h-48 overflow-hidden">
                <img
                  src={post.image}
                  alt={post.title}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-secondary via-secondary/50 to-transparent"></div>
                <div className={`absolute top-4 left-4 px-3 py-1 bg-gradient-to-r ${getCategoryColor(post.category)} rounded-full text-xs font-semibold text-white`}>
                  {post.category}
                </div>
              </div>

              <div className="p-6 space-y-4">
                <div className="flex items-center gap-4 text-xs text-text-muted">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {new Date(post.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {post.readTime}
                  </span>
                </div>

                <h3 className="text-xl font-bold group-hover:text-accent-teal transition-colors line-clamp-2">
                  {post.title}
                </h3>

                <p className="text-text-muted text-sm leading-relaxed line-clamp-3">
                  {post.excerpt}
                </p>

                <div className="flex flex-wrap gap-2">
                  {post.tags.map((tag, i) => (
                    <span key={i} className="flex items-center gap-1 text-xs text-accent-teal bg-accent-teal/10 px-2 py-1 rounded">
                      <Tag className="w-3 h-3" />
                      {tag}
                    </span>
                  ))}
                </div>

                <div className="pt-4 border-t border-tertiary">
                  <button className="flex items-center space-x-2 text-accent-teal hover:text-accent-purple transition-colors font-medium group">
                    <span>Read More</span>
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
              </div>
            </article>
          ))}
        </div>

        <div className="mt-16 text-center fade-in">
          <button className="btn-secondary">
            View All Articles
          </button>
        </div>
      </div>
    </section>
  );
}
