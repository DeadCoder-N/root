# Dead_Coderr - ASP.NET Core MVC Portfolio

This is an ASP.NET Core MVC version of the original React portfolio, maintaining 100% visual and functional parity.

## Features

- **Identical UI/UX**: Exact replica of the original React portfolio
- **Interactive Terminal**: Command-line interface with portfolio information
- **Contact Form**: Working contact form with database storage
- **Responsive Design**: Mobile-first responsive design
- **Smooth Animations**: CSS animations and transitions
- **Theme Support**: Dark theme with glassmorphism effects
- **SEO Optimized**: Server-side rendering for better SEO

## Tech Stack

- ASP.NET Core 8 MVC
- Entity Framework Core
- SQL Server LocalDB
- Custom CSS (converted from Tailwind)
- Vanilla JavaScript
- HTML5 & CSS3

## Getting Started

1. **Prerequisites**
   - .NET 8 SDK
   - SQL Server LocalDB (comes with Visual Studio)

2. **Installation**
   ```bash
   cd Dead_Coderr
   dotnet restore
   dotnet ef database update
   dotnet run
   ```

3. **Database Setup**
   The application uses Entity Framework Code First approach. The database will be created automatically on first run.

## Project Structure

```
Dead_Coderr/
├── Controllers/
│   └── HomeController.cs
├── Data/
│   └── ApplicationDbContext.cs
├── Models/
│   └── ContactMessage.cs
├── Views/
│   ├── Home/
│   │   └── Index.cshtml
│   └── Shared/
│       └── _Layout.cshtml
├── wwwroot/
│   ├── css/
│   │   └── site.css
│   ├── js/
│   │   └── site.js
│   └── images/
└── Program.cs
```

## Features Implemented

### ✅ Completed Sections
- Header with navigation and mobile menu
- Hero section with typing animation
- About section with statistics
- Interactive Terminal with commands
- Contact form with database integration
- Footer with social links

### 🚧 To Be Added (Future Updates)
- Skills section with progress bars
- Experience timeline
- Projects showcase
- CTF challenges section
- Security tools section
- Blog section

## Commands Available in Terminal

- `help` - Show available commands
- `about` - Learn about Nitesh
- `skills` - View technical skills
- `projects` - List featured projects
- `contact` - Get contact information
- `whoami` - Display user info
- `clear` - Clear terminal
- `hack` - Try the secret command
- `ls` - List files
- `pwd` - Show current directory
- `date` - Show current date

## Contact Form

The contact form stores messages in a SQL Server database using Entity Framework Core. Messages include:
- Name
- Email
- Subject
- Message
- Timestamp

## Styling

The project uses custom CSS converted from the original Tailwind CSS, maintaining:
- CSS custom properties for theming
- Glassmorphism effects
- Gradient text
- Smooth animations
- Responsive grid layouts
- Hover effects and transitions

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is for portfolio purposes. All rights reserved by Nitesh Sawardekar.

## Author

**Nitesh Sawardekar (Dead Coder)**
- Email: niteshsawardekar972@gmail.com
- GitHub: https://github.com/DeadCoder-N
- LinkedIn: https://www.linkedin.com/in/nitesh-sawardekar-39708a310/