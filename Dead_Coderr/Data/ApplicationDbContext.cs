using Dead_Coderr.Models;
using Microsoft.EntityFrameworkCore;

namespace Dead_Coderr.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) { }

        public DbSet<ContactMessage> ContactMessages { get; set; }
    }
}