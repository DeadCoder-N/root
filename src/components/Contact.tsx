import { useState } from 'react';
import { Mail, Send, CheckCircle, AlertCircle, MapPin, Phone } from 'lucide-react';
import { supabase } from '../lib/supabase';

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    setErrorMessage('');

    try {
      if (!supabase) {
        // Fallback: simulate success for demo purposes
        console.log('Contact form submission:', formData);
        setStatus('success');
        setFormData({ name: '', email: '', subject: '', message: '' });
        setTimeout(() => setStatus('idle'), 5000);
        return;
      }

      const { error } = await supabase
        .from('contact_messages')
        .insert([
          {
            name: formData.name,
            email: formData.email,
            subject: formData.subject,
            message: formData.message,
            created_at: new Date().toISOString(),
          },
        ]);

      if (error) throw error;

      setStatus('success');
      setFormData({ name: '', email: '', subject: '', message: '' });
      setTimeout(() => setStatus('idle'), 5000);
    } catch (error) {
      setStatus('error');
      setErrorMessage(error instanceof Error ? error.message : 'Failed to send message');
      setTimeout(() => setStatus('idle'), 5000);
    }
  };

  const contactInfo = [
    {
      icon: Mail,
      label: 'Email',
      value: 'niteshsawardekar972@gmail.com',
      href: 'mailto:niteshsawardekar972@gmail.com',
    },
    {
      icon: Phone,
      label: 'Phone',
      value: '+91 8454806491',
      href: 'tel:+91 8454806491',
    },
    {
      icon: MapPin,
      label: 'Location',
      value: 'Kalyan, India',
      href: null,
    },
  ];

  return (
    <section id="contact" className="py-20 bg-secondary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Get In <span className="gradient-text">Touch</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            Have a project in mind or want to discuss opportunities? Feel free to reach out!
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          <div className="space-y-8 fade-in">
            <div>
              <h3 className="text-2xl font-bold mb-4">Let's work together</h3>
              <p className="text-text-muted leading-relaxed">
                I'm always interested in hearing about new projects and opportunities.
                Whether you have a question or just want to say hi, I'll do my best to get back to you!
              </p>
            </div>

            <div className="space-y-6">
              {contactInfo.map((info, index) => (
                <div
                  key={index}
                  className="glass-card p-6 flex items-start space-x-4 group cursor-pointer"
                >
                  <div className="w-12 h-12 bg-gradient-to-r from-accent-teal to-accent-purple rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                    <info.icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <p className="text-text-muted text-sm mb-1">{info.label}</p>
                    {info.href ? (
                      <a
                        href={info.href}
                        className="text-lg font-semibold text-accent-teal hover:text-accent-purple transition-colors"
                      >
                        {info.value}
                      </a>
                    ) : (
                      <p className="text-lg font-semibold">{info.value}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div className="glass-card p-6">
              <h4 className="text-lg font-semibold mb-4">Why work with me?</h4>
              <ul className="space-y-3">
                {[
                  'Strong foundation in cybersecurity principles',
                  'Modern web development skills',
                  'Problem-solving mindset',
                  'Continuous learning and adaptation',
                  'Clear communication and collaboration',
                ].map((point, i) => (
                  <li key={i} className="flex items-start text-text-secondary text-sm">
                    <span className="text-accent-teal mr-2">▹</span>
                    {point}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="fade-in">
            <form onSubmit={handleSubmit} className="glass-card p-8 space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-text-secondary mb-2">
                  Name
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 bg-tertiary border border-tertiary focus:border-accent-teal rounded-lg outline-none transition-colors text-text-primary"
                  placeholder="Your name"
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-text-secondary mb-2">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 bg-tertiary border border-tertiary focus:border-accent-teal rounded-lg outline-none transition-colors text-text-primary"
                  placeholder="your.email@example.com"
                />
              </div>

              <div>
                <label htmlFor="subject" className="block text-sm font-medium text-text-secondary mb-2">
                  Subject
                </label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 bg-tertiary border border-tertiary focus:border-accent-teal rounded-lg outline-none transition-colors text-text-primary"
                  placeholder="What's this about?"
                />
              </div>

              <div>
                <label htmlFor="message" className="block text-sm font-medium text-text-secondary mb-2">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={5}
                  className="w-full px-4 py-3 bg-tertiary border border-tertiary focus:border-accent-teal rounded-lg outline-none transition-colors text-text-primary resize-none"
                  placeholder="Tell me more about your project..."
                ></textarea>
              </div>

              {status === 'success' && (
                <div className="flex items-center space-x-2 text-accent-green bg-accent-green/10 p-4 rounded-lg border border-accent-green/30">
                  <CheckCircle className="w-5 h-5" />
                  <span>Message sent successfully! I'll get back to you soon.</span>
                </div>
              )}

              {status === 'error' && (
                <div className="flex items-center space-x-2 text-accent-pink bg-accent-pink/10 p-4 rounded-lg border border-accent-pink/30">
                  <AlertCircle className="w-5 h-5" />
                  <span>{errorMessage || 'Failed to send message. Please try again.'}</span>
                </div>
              )}

              <button
                type="submit"
                disabled={status === 'loading'}
                className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {status === 'loading' ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Sending...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    <span>Send Message</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}
