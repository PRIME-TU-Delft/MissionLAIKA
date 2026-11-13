# 🚀 Mission LAIKA: Linear Algebra in Kinematics and Aerodynamics

Welcome to **Mission LAIKA**, a visual exploration of Linear Algebra through real-world applications in **kinematics** and **aerodynamics**. This project uses [Manim](https://www.manim.community/) to create mathematical animations that explain abstract concepts in a way that is easy to understand for **Aerospace Engineering** students.

Some animations are accompanied by Python exercises run using Google Colab.

---

## Current Case Studies

The animations include:

- Case Study 1: Cleared for take-off
- Case Study 4: Facing wind - I
- Case Study 5: Pitch perfect
- Case Study 6: Facing wind - II
- Case Study 8A: Modelling the airplane as a mass-spring system
- Case Study 8B: Navigating Subspaces
- Case Study 9A: will the wings fall off - I
- Case Study 9B: will the wings fall off - II
- Case Study 10: Swinging Back to Safety
- Case Study 12: Why Airplanes Don’t Twist
- Case Study 19: will the wings fall off? -revisited with beam

The Python exercises include:

- Case Study 15: Satellite Connection Back Online
- Case Study 19: Will the Wings Fall off Revisited

---

## Repository Structure

```
Mission-LAIKA/
├── CaseStudy1/
├── CaseStudy4/
├── CaseStudy5/
├── CaseStudy6/
├── CaseStudy8/
├── CaseStudy9/
├── CaseStudy10/
├── CaseStudy12/
├── CaseStudy19/
├── PythonExercises/        # Python notebooks to accompany animations
├── assets/                 # Images, SVGs used
├── requirements.txt        # Python dependencies
└── README.md               # Project overview
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Mission-LAIKA.git
cd Mission-LAIKA
```

### 2. Install Manim

The instructions for installing Manim can be found on [Manim Community Edition](https://docs.manim.community/en/stable/installation.html). 


### 3. Install uv

This project uses [uv](https://docs.astral.sh/uv/) to manage Python and dependencies.

```bash
# macOS / Linux / WSL
curl -LsSf https://astral.sh/uv/install.sh | sh
```


### 4. Install system libraries

Manim needs Cairo, Pango and ffmpeg.

**WSL / Ubuntu / Debian**
```bash
sudo apt update
sudo apt install libcairo2-dev libpango1.0-dev ffmpeg pkg-config build-essential
```

**macOS**
```bash
brew install cairo pango pkg-config ffmpeg
```

LaTeX is only needed if your scenes use `Tex` / `MathTex`. If they do, you can follow the instructions on [Manim Community Edition](https://docs.manim.community/en/stable/installation.html).

### 5. Install the project

From the repo root:

```bash
uv sync
```
You can run `uv run manim checkhealth` to verify your installation.


### 6. Render an animation

Navigate to the **animation folder**, e.g.:

```bash
cd CaseStudy1
```

and run:

```bash
uv run manim -p beginning.py
```

*Note: Always run commands through `uv run` so they use the project environment.*

Quality flags: `-ql` (480p), `-qm` (720p), `-qh` (1080p), `-qk` (4K). Output goes to the `media/` folder.

--- 
## Managing dependencies

Commit both `pyproject.toml` and `uv.lock` whenever they change. Don't use `pip install` in this project.

---

## Finished animations

[Case Study 1: Cleared for take-off](https://www.youtube.com/watch?v=ywKGTBe20Lc)

[Case Study 4: Facing wind - I](https://youtu.be/JF9Xfm3LzTk)

[Case Study 5: Pitch perfect](https://youtu.be/yczylyVWd_8)

[Case Study 6: Facing wind - II](https://youtu.be/VBQISSp7Zcs)

[Case Study 8A: Modelling the airplane as a mass-spring system](https://youtu.be/oDWK9nEBMj0)

[Case Study 8B: Navigating Subspaces](https://youtu.be/f3VHGpBfLKM)

[Case Study 9A: will the wings fall off - I](https://youtu.be/2SgTFmlUcaM)

[Case Study 9B: will the wings fall off - II](https://youtu.be/WV6hbjuTdVs)

[Case Study 10: Swinging Back to Safety](https://youtu.be/03BW-PDf1yM)

[Case Study 12: Why Airplanes Don’t Twist](https://youtu.be/kmkQi8FLybM)

[Case Study 19: will the wings fall off? -revisited with beam](https://youtu.be/bS8eDBAfS4w)


---

## Contributing

Pull requests are welcome! If you have ideas for new scenes or applications, open an issue or submit a PR.

---

## Authors

Animations and Python notebooks made by [Jakub Fręchowicz](https://jakubfrechowicz.com) and [Stella Schultz](https://github.com/smarlene).

Feel free to reach out!
