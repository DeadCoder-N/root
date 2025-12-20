using Dead_Coderr.Data;
using Dead_Coderr.Models;
using Microsoft.AspNetCore.Mvc;

namespace Dead_Coderr.Controllers
{
    public class HomeController : Controller
    {
        private readonly ApplicationDbContext _context;

        public HomeController(ApplicationDbContext context)
        {
            _context = context;
        }

        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Contact(ContactMessage message)
        {
            if (ModelState.IsValid)
            {
                _context.ContactMessages.Add(message);
                await _context.SaveChangesAsync();
                return Json(new { success = true, message = "Message sent successfully!" });
            }
            return Json(new { success = false, message = "Please fill all required fields." });
        }
    }
}