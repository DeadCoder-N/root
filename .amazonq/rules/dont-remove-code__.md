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

## RULE 3: Styling Changes - When to Delete vs Comment

### ✅ Can DELETE Directly (Small/Medium Styling):

**Single Property Changes:**
- Colors: `bg-blue-500` → `bg-teal-500`
- Spacing: `px-4` → `px-6`, `gap-4` → `gap-6`
- Positioning: `top-4` → `top-6`, `left-2` → `left-4`
- Sizes: `w-32` → `w-40`, `h-20` → `h-24`
- Text: `text-2xl` → `text-3xl`, `font-normal` → `font-bold`
- Borders: `border-2` → `border-4`
- Opacity: `opacity-50` → `opacity-70`
- Radius: `rounded-md` → `rounded-lg`

**Few Properties on ONE Element:**
```tsx
// Change 2-5 properties on one element - DELETE
<div className="p-4 bg-blue text-xl">
↓
<div className="p-6 bg-teal text-2xl">  ✅ Just change it
```

**Small Localized Changes:**
- One card's styling
- One button's appearance
- One section's colors

### ❌ MUST COMMENT OUT (Large Styling/Redesign):

**Entire Section Redesign:**
```tsx
// Whole blog section theme change
// Multiple elements, layout changes, complete redesign
<section id="blog" className="...">
  <div>...</div>
  <article>...</article>
  <footer>...</footer>
</section>
```
**→ COMMENT OUT entire old section**

**Multiple Elements Changed Together:**
- Redesigning header + navigation + footer
- Changing layout of multiple cards
- Complete theme overhaul

**Structural + Styling:**
```tsx
// Changing from grid to flex + colors
<div className="grid grid-cols-3 gap-4">
↓
<div className="flex flex-wrap space-x-6">
```
**→ COMMENT OUT (structure changed)**

### Decision Rule:
**Ask:** "How many elements am I changing?"
- **1 element, few properties** → DELETE old, write new
- **Multiple elements, entire section** → COMMENT OUT old, add new

**Ask:** "Is this a complete redesign?"
- **No, just tweaking** → DELETE
- **Yes, redesigning** → COMMENT OUT

---

## RULE 4: Structural/Functional Changes - Always Comment

### ❌ MUST ALWAYS COMMENT OUT:
- Changing element type: `<button>` → `<Button>`
- Changing input type: `type="text"` → `type="email"`
- Adding/removing attributes: adding `onClick`, `onChange`
- Changing structure: `<div>` → `<section>`
- Replacing components: `OldButton` → `NewButton`
- Adding/removing child elements
- Changing logic: if conditions, loops
- Changing event handlers
- Modifying functions/hooks

---

## Summary

**Small styling (1 element, few properties)** → DELETE
**Large styling (entire section, multiple elements)** → COMMENT OUT
**Structural/functional changes** → ALWAYS COMMENT OUT
**Entire files** → ARCHIVE to `src/archived/`
**Exception:** Typos only
