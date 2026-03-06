# Code Modification Policy

## RULE 1: Never Delete Code - Always Comment Out

When modifying or replacing code inside a file:

### ❌ NEVER:
- Delete old code
- Remove old functions/components
- Erase previous implementations

### ✅ ALWAYS:
1. Comment out the old code with date and reason
2. Add new code below (NO comment block on new code)
3. Keep both versions visible forever

### Format:
```
// ============================================
// OLD CODE - Commented out YYYY-MM-DD
// Reason: [why it was changed]
// ============================================
// [old code here]

[new code here - clean, no comment block]
```

### Exception:
- **Typos only** - Can delete typos in variable/function names directly

---

## RULE 2: Never Delete Files - Always Archive

When replacing entire files:

### ❌ NEVER:
- Delete old files
- Remove old components/modules

### ✅ ALWAYS:
1. Move old file to `src/archived/` folder (central archive)
2. Keep original folder structure inside archived
3. Rename with `.old.YYYY-MM-DD` suffix
4. Create new file in original location

### Example:
```
Before:
src/components/Header.tsx

After:
src/archived/components/Header.tsx.old.2024-01-15
src/components/Header.tsx (new file)
```

### Archive Structure:
```
src/
├── archived/                    ← ONE central archive folder
│   ├── components/
│   │   └── [old component files]
│   ├── hooks/
│   │   └── [old hook files]
│   └── lib/
│       └── [old utility files]
├── components/                  ← Active files
├── hooks/
└── lib/
```

---

## RULE 3: Formatting Changes - When to Delete vs Comment

### ✅ Can DELETE Directly (Small Visual Changes):
- Borders: `border-2` → `border-4`
- Spacing: `px-4` → `px-6`, `gap-4` → `gap-6`
- Positioning: `top-4` → `top-6`, `left-2` → `left-4`
- Colors: `bg-blue-500` → `bg-teal-500`
- Sizes: `w-32` → `w-40`, `h-20` → `h-24`
- Text: `text-2xl` → `text-3xl`, `font-normal` → `font-bold`
- Opacity: `opacity-50` → `opacity-70`
- Radius: `rounded-md` → `rounded-lg`

### ❌ MUST COMMENT OUT (Structural/Functional Changes):
- Changing element type: `<button>` → `<Button>`
- Changing input type: `type="text"` → `type="email"`
- Adding/removing attributes: adding `onClick`, `onChange`
- Changing structure: `<div>` → `<section>`
- Replacing components: `OldButton` → `NewButton`
- Adding/removing child elements
- Changing logic: if conditions, loops
- Changing event handlers

### Simple Test:
**Ask:** "Did I change WHAT it is, or just HOW it looks?"
- **HOW it looks** (styling only) → DELETE old, write new
- **WHAT it is** (functionality/structure) → COMMENT OUT old, add new

---

## Summary

- Never delete code → Comment out (only old code, keep new code clean)
- Never delete files → Archive to central `src/archived/` folder
- Keep everything forever
- Only exception: Typos and small styling changes
