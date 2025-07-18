---
title: "Extending McRogueFace with C++"
description: "A comprehensive guide to creating C++ extensions for the McRogueFace engine"
layout: default
---

# Extending McRogueFace with C++

**Make 2D games with Python** - No C++ required!

---

[**Source Code**](https://github.com/jmccardle/McRogueFace) • [**Downloads**](https://github.com/jmccardle/McRogueFace/releases) • [**Quickstart**](https://mcrogueface.github.io/quickstart) • [**Tutorials**](https://mcrogueface.github.io/tutorials) • [**API Reference**](https://mcrogueface.github.io/api-reference) • [**Cookbook**](https://mcrogueface.github.io/cookbook) • **[C++ Extensions](https://mcrogueface.github.io/extending-cpp)**

---

> **🚀 Take your game to the next level by extending the engine with custom C++ components**

## Table of Contents

1. [Introduction: When and Why to Extend in C++](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Setting Up Your Development Environment](#development-setup)
4. [Understanding the Codebase Structure](#codebase-structure)
5. [Creating a New UI Element](#creating-ui-element)
6. [Adding Python Bindings](#python-bindings)
7. [Testing Your Extension](#testing-extension)
8. [Case Study: Creating a Custom Particle System](#case-study-particles)
9. [Best Practices and Common Pitfalls](#best-practices)

## Introduction: When and Why to Extend in C++ {#introduction}

While McRogueFace provides a powerful Python API for game development, there are scenarios where extending the engine in C++ provides significant benefits:

### When to Extend in C++

- **Code That Runs Every Frame**: If you need logic to execute continuously without timer overhead, implement it in C++
- **Hardware Integration**: Custom input devices, specialized rendering techniques
- **Engine Features**: New UI components, audio effects, rendering pipelines
- **Library Integration**: Bringing in external C++ libraries for physics, networking, etc.

### Benefits of C++ Extensions

- **Frame-Perfect Execution**: Code that needs to run every single frame should be in C++ to avoid timer overhead
- **Memory Control**: Precise memory management for resource-intensive features
- **Type Safety**: Compile-time checking and better IDE support
- **Engine Integration**: Seamless integration with the existing C++ codebase

Note: Python with NumPy can achieve excellent performance for many tasks. The main reason to use C++ is when you need code to run every frame without the overhead of timers - for this use case, implement directly in C++.

## Architecture Overview {#architecture-overview}

McRogueFace follows a layered architecture that makes it extensible:

```
┌─────────────────────────────────────────────────┐
│             Python Game Scripts                  │
│         (game.py, entities.py, etc.)            │
├─────────────────────────────────────────────────┤
│          Python API Layer (mcrfpy)              │
│        (McRFPy_API.cpp, bindings)               │
├─────────────────────────────────────────────────┤
│           Core Engine Components                 │
│   ┌─────────────┬─────────────┬─────────────┐  │
│   │  UI System  │   Scene     │   Entity    │  │
│   │  (UIFrame,  │  Manager    │   System    │  │
│   │  UISprite)  │             │             │  │
│   └─────────────┴─────────────┴─────────────┘  │
├─────────────────────────────────────────────────┤
│              SFML Framework                      │
│    (Graphics, Audio, Window, System)            │
└─────────────────────────────────────────────────┘
```

### Key Components

1. **UIDrawable Base Class**: Abstract base class for all visual elements
   - Derived classes: `UIFrame`, `UISprite`, `UICaption`, and `UIGrid`
   - Can be drawn directly on scenes or nested within UIFrame containers
   - Handles click event routing through the `click_at()` virtual method
   - Click events propagate from top-level elements down through nested children

2. **Scene System**: Manages game states and transitions
   - `Scene` base class for C++ scenes
   - `PyScene` for Python-controlled scenes with UI element management

3. **Python Bindings**: CPython API integration for scripting
   - McRogueFace operates on an "honor system" - Python scripts must return control
   - The engine calls scripts when starting, but scripts must return to allow the game loop to run
   - If a script doesn't return (e.g., infinite loop), McRogueFace will hang
   - Event handlers can register callbacks and modify UI elements during execution

4. **Resource Management**: Textures, fonts, and audio handling

## Setting Up Your Development Environment {#development-setup}

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get install -y \
    build-essential \
    cmake \
    libsfml-dev \
    python3.12-dev \
    git


# Windows (using vcpkg)
vcpkg install sfml
```

> **Note**: On Windows, when building with CMake, use the correct command:
> 
> ```bash
> cmake --build . --config Release --parallel
> ```

### Building McRogueFace

1. Clone the repository:
```bash
git clone https://github.com/mcrogueface/engine.git
cd engine
git submodule update --init --recursive
```

2. Build the project:
```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Debug
make -j$(nproc)
```

3. Set up development environment:
```bash
# Create a development branch
git checkout -b feature/my-extension

# Set up your IDE (VS Code example)
code .
```

### Recommended IDE Setup

For VS Code, install these extensions:
- C/C++ (Microsoft)
- CMake Tools
- Python

Create `.vscode/c_cpp_properties.json`:
```json
{
    "configurations": [{
        "name": "Linux",
        "includePath": [
            "${workspaceFolder}/src/**",
            "${workspaceFolder}/deps/**",
            "/usr/include/python3.12"
        ],
        "defines": [],
        "compilerPath": "/usr/bin/g++",
        "cStandard": "c17",
        "cppStandard": "c++20"
    }]
}
```

## Understanding the Codebase Structure {#codebase-structure}

```
McRogueFace/
├── src/                      # C++ source files
│   ├── UI*.h/cpp            # UI component files
│   ├── Py*.h/cpp            # Python binding helpers
│   ├── McRFPy_API.h/cpp     # Main Python API
│   ├── Scene.h/cpp          # Scene management
│   ├── PyScene.h/cpp        # Python scene management
│   └── main.cpp             # Entry point
├── deps/                     # Dependencies
│   ├── cpython/             # Python headers
│   └── libtcod/             # Roguelike utilities
├── assets/                   # Game assets
├── scripts/                  # Python game scripts
└── CMakeLists.txt           # Build configuration
```

### Key File Patterns

- **UI Components**: `UI[Component].h/cpp` (e.g., UIFrame, UISprite)
- **Python Types**: `Py[Type].h` (e.g., PyTexture, PyColor)
- **Python Objects**: `typedef struct { PyObject_HEAD ... } Py[Type]Object;`

## Creating a New UI Element {#creating-ui-element}

Let's create a custom progress bar component step by step.

### Step 1: Define the C++ Class

Create `src/UIProgressBar.h`:

```cpp
#pragma once
#include "UIDrawable.h"
#include "PyColor.h"
#include <SFML/Graphics.hpp>

class UIProgressBar : public UIDrawable {
private:
    sf::RectangleShape background;
    sf::RectangleShape fill;
    float progress = 0.0f;  // 0.0 to 1.0
    float width, height;
    
public:
    UIProgressBar(float x, float y, float w, float h);
    
    // UIDrawable interface
    void render(sf::Vector2f position, sf::RenderTarget& target) override;
    PyObjectsEnum derived_type() override { return UIPROGRESSBAR; }
    UIDrawable* click_at(sf::Vector2f point) override;
    
    // Phase 1 implementations
    sf::FloatRect get_bounds() const override;
    void move(float dx, float dy) override;
    void resize(float w, float h) override;
    
    // Progress bar specific
    void setProgress(float value);
    float getProgress() const { return progress; }
    void setFillColor(const sf::Color& color);
    void setBackgroundColor(const sf::Color& color);
    
    // Animation support
    bool setProperty(const std::string& name, float value) override;
    bool getProperty(const std::string& name, float& value) const override;
};
```

### Step 2: Add to PyObjectsEnum

> **⚠️ Warning**: Creating new UI elements by adding to PyObjectsEnum has never been tested and may not work as expected. Consider using the alternative approach described in [Best Practices](#best-practices) instead.

Update `src/UIDrawable.h`:

```cpp
enum PyObjectsEnum : int
{
    UIFRAME = 1,
    UICAPTION,
    UISPRITE,
    UIGRID,
    UIPROGRESSBAR  // Add this
};
```

### Step 3: Implement the Class

Create `src/UIProgressBar.cpp`:

```cpp
#include "UIProgressBar.h"

UIProgressBar::UIProgressBar(float x, float y, float w, float h) 
    : width(w), height(h) {
    position = sf::Vector2f(x, y);
    
    // Set up background
    background.setSize(sf::Vector2f(width, height));
    background.setFillColor(sf::Color(50, 50, 50, 255));
    background.setOutlineColor(sf::Color(100, 100, 100, 255));
    background.setOutlineThickness(2.0f);
    
    // Set up fill
    fill.setSize(sf::Vector2f(0, height));
    fill.setFillColor(sf::Color(0, 255, 0, 255));
}

void UIProgressBar::render(sf::Vector2f position, sf::RenderTarget& target) {
    if (!visible) return;
    
    // Apply opacity
    auto bgColor = background.getFillColor();
    bgColor.a = static_cast<sf::Uint8>(255 * opacity);
    background.setFillColor(bgColor);
    
    auto fillColor = fill.getFillColor();
    fillColor.a = static_cast<sf::Uint8>(255 * opacity);
    fill.setFillColor(fillColor);
    
    // Position elements
    sf::Vector2f absolute_pos = position + this->position;
    background.setPosition(absolute_pos);
    fill.setPosition(absolute_pos);
    
    // Draw
    target.draw(background);
    if (progress > 0.0f) {
        target.draw(fill);
    }
}

UIDrawable* UIProgressBar::click_at(sf::Vector2f point) {
    if (background.getGlobalBounds().contains(point)) {
        return this;
    }
    return nullptr;
}

void UIProgressBar::setProgress(float value) {
    progress = std::max(0.0f, std::min(1.0f, value));
    fill.setSize(sf::Vector2f(width * progress, height));
}

sf::FloatRect UIProgressBar::get_bounds() const {
    return sf::FloatRect(position.x, position.y, width, height);
}

void UIProgressBar::move(float dx, float dy) {
    position.x += dx;
    position.y += dy;
}

void UIProgressBar::resize(float w, float h) {
    width = w;
    height = h;
    background.setSize(sf::Vector2f(width, height));
    setProgress(progress);  // Update fill size
}

bool UIProgressBar::setProperty(const std::string& name, float value) {
    if (name == "progress") {
        setProgress(value);
        return true;
    }
    return false;
}

bool UIProgressBar::getProperty(const std::string& name, float& value) const {
    if (name == "progress") {
        value = progress;
        return true;
    }
    return false;
}
```

## Adding Python Bindings {#python-bindings}

> **⚠️ Warning**: This section on adding Python bindings is largely untested and may be overly complex. The binding process involves many intricate steps that can easily go wrong. Consider using existing UI elements and extending them in Python instead.

Now let's expose our progress bar to Python.

### Step 1: Define Python Type Structure

Create the Python object structure in `src/UIProgressBar.h`:

```cpp
// Python object structure
typedef struct {
    PyObject_HEAD
    std::shared_ptr<UIProgressBar> data;
} PyUIProgressBarObject;

// Forward declarations
extern PyMethodDef UIProgressBar_methods[];
extern PyGetSetDef UIProgressBar_getsetters[];
```

### Step 2: Implement Python Methods

Add to `src/UIProgressBar.cpp`:

```cpp
// Python property getters/setters
static PyObject* UIProgressBar_get_progress(PyObject* self, void* closure) {
    auto obj = (PyUIProgressBarObject*)self;
    return PyFloat_FromDouble(obj->data->getProgress());
}

static int UIProgressBar_set_progress(PyObject* self, PyObject* value, void* closure) {
    auto obj = (PyUIProgressBarObject*)self;
    if (!PyFloat_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "progress must be a float");
        return -1;
    }
    obj->data->setProgress(PyFloat_AsDouble(value));
    return 0;
}

// Python methods
static PyObject* UIProgressBar_setFillColor(PyObject* self, PyObject* args) {
    PyUIProgressBarObject* obj = (PyUIProgressBarObject*)self;
    PyObject* color_obj;
    
    if (!PyArg_ParseTuple(args, "O", &color_obj)) {
        return NULL;
    }
    
    // Convert Python color to sf::Color
    sf::Color color;
    if (!PyColor::from_python(color_obj, color)) {
        return NULL;
    }
    
    obj->data->setFillColor(color);
    Py_RETURN_NONE;
}

// Method definitions
PyMethodDef UIProgressBar_methods[] = {
    {"setFillColor", UIProgressBar_setFillColor, METH_VARARGS,
     "setFillColor(color: Color) -> None\n\n"
     "Set the fill color of the progress bar.\n\n"
     "Args:\n"
     "    color: Color object for the fill"},
    {NULL}
};

// Property definitions
PyGetSetDef UIProgressBar_getsetters[] = {
    {"progress", UIProgressBar_get_progress, UIProgressBar_set_progress,
     "Current progress value (0.0 to 1.0)", NULL},
    {"x", UIDrawable::get_float_member, UIDrawable::set_float_member,
     "X position in pixels", (void*)offsetof(UIProgressBar, position.x)},
    {"y", UIDrawable::get_float_member, UIDrawable::set_float_member,
     "Y position in pixels", (void*)offsetof(UIProgressBar, position.y)},
    {NULL}
};

// Init function
static int UIProgressBar_init(PyObject* self, PyObject* args, PyObject* kwds) {
    auto obj = (PyUIProgressBarObject*)self;
    float x = 0, y = 0, w = 100, h = 20;
    
    static char* kwlist[] = {"x", "y", "w", "h", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|ffff", kwlist,
                                     &x, &y, &w, &h)) {
        return -1;
    }
    
    obj->data = std::make_shared<UIProgressBar>(x, y, w, h);
    return 0;
}
```

### Step 3: Register the Type

Create the type definition in a namespace:

```cpp
namespace mcrfpydef {
    static PyTypeObject PyUIProgressBarType = {
        .ob_base = {.ob_base = {.ob_refcnt = 1, .ob_type = NULL}, .ob_size = 0},
        .tp_name = "mcrfpy.ProgressBar",
        .tp_basicsize = sizeof(PyUIProgressBarObject),
        .tp_itemsize = 0,
        .tp_dealloc = (destructor)[](PyObject* self) {
            auto obj = (PyUIProgressBarObject*)self;
            obj->data.reset();
            Py_TYPE(self)->tp_free(self);
        },
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_doc = PyDoc_STR("ProgressBar(x=0, y=0, w=100, h=20)\n\n"
                           "A progress bar UI element.\n\n"
                           "Args:\n"
                           "    x, y: Position in pixels\n"
                           "    w, h: Size in pixels"),
        .tp_methods = UIProgressBar_methods,
        .tp_getset = UIProgressBar_getsetters,
        .tp_base = &mcrfpydef::PyDrawableType,
        .tp_init = UIProgressBar_init,
        .tp_new = [](PyTypeObject* type, PyObject* args, PyObject* kwds) -> PyObject* {
            auto self = (PyUIProgressBarObject*)type->tp_alloc(type, 0);
            if (self) self->data = std::make_shared<UIProgressBar>(0, 0, 100, 20);
            return (PyObject*)self;
        }
    };
}
```

### Step 4: Register with Module

Update `src/McRFPy_API.cpp` to register the new type:

```cpp
// In api_init() function, add:
if (PyType_Ready(&mcrfpydef::PyUIProgressBarType) < 0) {
    PyErr_SetString(PyExc_RuntimeError, "Failed to ready ProgressBar type");
    return;
}

Py_INCREF(&mcrfpydef::PyUIProgressBarType);
PyModule_AddObject(mcrf_module, "ProgressBar", 
                   (PyObject*)&mcrfpydef::PyUIProgressBarType);
```

### Step 5: Update Build System

Add the new files to `CMakeLists.txt` or ensure they're picked up by the glob pattern.

## Testing Your Extension {#testing-extension}

Create a test script to verify your progress bar works:

```python
# tests/test_progress_bar.py
import mcrfpy
from mcrfpy import ProgressBar, Frame, Color
import sys

def test_progress_bar():
    """Test the custom progress bar implementation"""
    
    # Create a test scene
    mcrfpy.createScene("test")
    
    # Create a frame to hold our progress bar
    frame = Frame(100, 100, 400, 300)
    frame.fill_color = Color(20, 20, 20, 255)
    
    # Create progress bars
    progress1 = ProgressBar(50, 50, 300, 30)
    progress1.progress = 0.0
    progress1.setFillColor(Color(0, 255, 0, 255))
    
    progress2 = ProgressBar(50, 100, 300, 30)
    progress2.progress = 0.5
    progress2.setFillColor(Color(255, 255, 0, 255))
    
    progress3 = ProgressBar(50, 150, 300, 30)
    progress3.progress = 1.0
    progress3.setFillColor(Color(255, 0, 0, 255))
    
    # Add to frame
    frame.children.append(progress1)
    frame.children.append(progress2)
    frame.children.append(progress3)
    
    # Add frame to scene
    ui = mcrfpy.sceneUI("test")
    ui.append(frame)
    
    # Animate progress bars
    def update_progress(elapsed):
        # Increment first progress bar
        progress1.progress = min(1.0, progress1.progress + 0.01)
        
        # Pulse second progress bar
        import math
        progress2.progress = abs(math.sin(elapsed * 2))
        
        # Check if done
        if progress1.progress >= 1.0:
            print("PASS: Progress bar animation completed")
            sys.exit(0)
    
    # Set timer for animation
    mcrfpy.setTimer("animate", update_progress, 16)  # ~60 FPS
    
    # Switch to test scene
    mcrfpy.setScene("test")

# Run test
test_progress_bar()
```

Run the test:
```bash
cd build
./mcrogueface --exec ../tests/test_progress_bar.py
```

## Case Study: Creating a Custom Particle System {#case-study-particles}

Let's build a more complex extension - a particle system for visual effects.

### Design Overview

Our particle system will:
- Manage thousands of particles efficiently
- Support different particle behaviors (gravity, wind, etc.)
- Integrate with the animation system
- Provide Python control over particle properties

### Implementation

```cpp
// src/UIParticleSystem.h
#pragma once
#include "UIDrawable.h"
#include <vector>
#include <random>

struct Particle {
    sf::Vector2f position;
    sf::Vector2f velocity;
    sf::Color color;
    float lifetime;
    float age;
    float size;
};

class UIParticleSystem : public UIDrawable {
private:
    std::vector<Particle> particles;
    std::vector<sf::Vertex> vertices;  // For batch rendering
    
    // Emitter properties
    sf::Vector2f emission_area;
    float emission_rate = 10.0f;
    float emission_timer = 0.0f;
    
    // Particle properties
    float initial_velocity = 100.0f;
    float velocity_variation = 50.0f;
    sf::Vector2f gravity = {0, 100};
    float particle_lifetime = 2.0f;
    float particle_size = 2.0f;
    
    // System state
    bool emitting = true;
    std::mt19937 rng;
    std::uniform_real_distribution<float> dist;
    
    void emitParticle();
    void updateParticle(Particle& p, float dt);
    
public:
    UIParticleSystem(float x, float y);
    
    void update(float dt);
    void render(sf::Vector2f position, sf::RenderTarget& target) override;
    PyObjectsEnum derived_type() override { return UIPARTICLESYSTEM; }
    
    // Control methods
    void start() { emitting = true; }
    void stop() { emitting = false; }
    void burst(int count);
    void clear() { particles.clear(); }
    
    // Property access
    void setGravity(float x, float y) { gravity = {x, y}; }
    void setEmissionRate(float rate) { emission_rate = rate; }
    void setParticleLifetime(float time) { particle_lifetime = time; }
};
```

Implementation details:

```cpp
// src/UIParticleSystem.cpp
#include "UIParticleSystem.h"

UIParticleSystem::UIParticleSystem(float x, float y) 
    : rng(std::random_device{}()), dist(0.0f, 1.0f) {
    position = sf::Vector2f(x, y);
    emission_area = sf::Vector2f(10, 10);
}

void UIParticleSystem::emitParticle() {
    Particle p;
    
    // Random position within emission area
    p.position = position + sf::Vector2f(
        (dist(rng) - 0.5f) * emission_area.x,
        (dist(rng) - 0.5f) * emission_area.y
    );
    
    // Random velocity
    float angle = dist(rng) * 2 * M_PI;
    float speed = initial_velocity + (dist(rng) - 0.5f) * velocity_variation;
    p.velocity = sf::Vector2f(cos(angle) * speed, sin(angle) * speed);
    
    // Initial properties
    p.color = sf::Color(255, 200, 100, 255);
    p.lifetime = particle_lifetime;
    p.age = 0.0f;
    p.size = particle_size;
    
    particles.push_back(p);
}

void UIParticleSystem::update(float dt) {
    // Emit new particles
    if (emitting) {
        emission_timer += dt;
        float emit_interval = 1.0f / emission_rate;
        
        while (emission_timer >= emit_interval) {
            emitParticle();
            emission_timer -= emit_interval;
        }
    }
    
    // Update existing particles
    for (auto it = particles.begin(); it != particles.end();) {
        updateParticle(*it, dt);
        
        if (it->age >= it->lifetime) {
            it = particles.erase(it);
        } else {
            ++it;
        }
    }
    
    // Prepare vertices for rendering
    vertices.clear();
    vertices.reserve(particles.size() * 6);  // 2 triangles per particle
    
    for (const auto& p : particles) {
        float alpha = 1.0f - (p.age / p.lifetime);
        sf::Color color = p.color;
        color.a = static_cast<sf::Uint8>(255 * alpha * opacity);
        
        // Create a quad with two triangles
        float half_size = p.size / 2.0f;
        sf::Vector2f tl = p.position + sf::Vector2f(-half_size, -half_size);
        sf::Vector2f tr = p.position + sf::Vector2f(half_size, -half_size);
        sf::Vector2f br = p.position + sf::Vector2f(half_size, half_size);
        sf::Vector2f bl = p.position + sf::Vector2f(-half_size, half_size);
        
        // Triangle 1
        vertices.emplace_back(tl, color);
        vertices.emplace_back(tr, color);
        vertices.emplace_back(br, color);
        
        // Triangle 2
        vertices.emplace_back(tl, color);
        vertices.emplace_back(br, color);
        vertices.emplace_back(bl, color);
    }
}

void UIParticleSystem::updateParticle(Particle& p, float dt) {
    // Apply physics
    p.velocity += gravity * dt;
    p.position += p.velocity * dt;
    
    // Age particle
    p.age += dt;
    
    // Color fade (example: fade from yellow to red)
    float age_ratio = p.age / p.lifetime;
    p.color.g = static_cast<sf::Uint8>(200 * (1.0f - age_ratio));
}

void UIParticleSystem::render(sf::Vector2f offset, sf::RenderTarget& target) {
    if (!visible || vertices.empty()) return;
    
    // Apply position offset to all vertices
    sf::Transform transform;
    transform.translate(offset);
    
    // Draw all particles in one batch
    target.draw(vertices.data(), vertices.size(), sf::Triangles, transform);
}
```

### Python Integration

The Python bindings follow the same pattern as before, but with additional methods:

```python
# Example usage in Python
import mcrfpy
from mcrfpy import ParticleSystem, Frame

# Create a particle system
particles = ParticleSystem(400, 300)
particles.setGravity(0, 200)  # Downward gravity
particles.setEmissionRate(50)  # 50 particles per second
particles.setParticleLifetime(3.0)  # 3 second lifetime

# Add to scene
frame = Frame(0, 0, 800, 600)
frame.children.append(particles)

# Control emission
def on_click(x, y, button):
    if button == 1:  # Left click
        particles.burst(100)  # Emit 100 particles at once
    elif button == 3:  # Right click
        particles.stop()  # Stop emitting

frame.click = on_click
```

## Best Practices and Common Pitfalls {#best-practices}

### Alternative to Creating New UI Elements

> **Recommended Approach**: Instead of creating entirely new UI element types (which requires modifying PyObjectsEnum and has never been tested), consider configuring existing `Frame` elements and overriding their render methods:

```python
# Create a custom progress bar using Frame
class ProgressBar:
    def __init__(self, x, y, width, height):
        self.frame = mcrfpy.Frame(x, y, width, height)
        self.frame.fill_color = (50, 50, 50)  # Background
        self.frame.outline = 2
        self.frame.outline_color = (100, 100, 100)
        
        # Create fill as a child frame
        self.fill = mcrfpy.Frame(2, 2, 0, height - 4)
        self.fill.fill_color = (0, 255, 0)
        self.frame.children.append(self.fill)
        
        self._progress = 0.0
    
    @property
    def progress(self):
        return self._progress
    
    @progress.setter
    def progress(self, value):
        self._progress = max(0.0, min(1.0, value))
        # Update fill width
        self.fill.w = (self.frame.w - 4) * self._progress
```

This approach:
- Works with the existing codebase
- Requires no C++ modifications
- Is fully tested and supported
- Can be extended with Python inheritance

### Memory Management

**✅ DO:**
- Use `std::shared_ptr` for objects shared between C++ and Python
- Clean up resources in destructors
- Use RAII principles

**❌ DON'T:**
- Store raw pointers to Python objects without proper reference counting
- Forget to reset shared_ptrs in Python object destructors
- Create circular references between C++ and Python objects

### Python Integration

**✅ DO:**
```cpp
// Register with Python object cache for proper type preservation
static PyObject* create_custom_element(PyObject* self, PyObject* args) {
    auto element = std::make_shared<UICustomElement>();
    
    // CRITICAL: Without this, derived types are lost!
    // The Python object cache maintains weak references
    auto py_obj = (PyUICustomElementObject*)type->tp_alloc(type, 0);
    py_obj->data = element;
    
    // Register in cache to preserve type information
    PythonObjectCache::register_object(element.get(), (PyObject*)py_obj);
    
    return (PyObject*)py_obj;
}
```

**Example: Python Object Cache Requirements**

Extension classes must properly interact with the Python object cache:

```cpp
// In your custom element's Python getter
static PyObject* UICustomElement_get_child(PyObject* self, void* closure) {
    auto obj = (PyUICustomElementObject*)self;
    auto child = obj->data->getChild();
    
    // Check cache first - this preserves derived Python types!
    PyObject* cached = PythonObjectCache::get(child.get());
    if (cached) {
        Py_INCREF(cached);
        return cached;
    }
    
    // Create new Python object and cache it
    auto py_child = create_python_wrapper(child);
    PythonObjectCache::register_object(child.get(), py_child);
    return py_child;
}
```

Without proper cache management:
- Python subclasses of your C++ types will lose their Python-specific attributes
- Type information gets lost when objects round-trip through C++
- `isinstance()` checks may fail unexpectedly

**✅ DO:**
```cpp
// Proper reference counting
static PyObject* get_property(PyObject* self, void* closure) {
    PyObject* result = PyFloat_FromDouble(value);
    return result;  // New reference
}

// Proper error handling
if (!PyArg_ParseTuple(args, "ff", &x, &y)) {
    return NULL;  // Python exception already set
}
```

**❌ DON'T:**
```cpp
// Missing incref - will crash!
static PyObject* bad_getter(PyObject* self, void* closure) {
    return some_cached_object;  // Missing Py_INCREF!
}

// Missing error check
float x = PyFloat_AsDouble(obj);  // Could be -1 with error set!
```

### Performance Considerations

1. **Batch Rendering**: Use vertex arrays for many similar objects
2. **Dirty Flags**: Only update when properties change
3. **Object Pooling**: Reuse objects instead of creating/destroying
4. **Profile First**: Use profiling tools before optimizing

### Thread Safety

McRogueFace runs Python in a single thread. When adding C++ extensions:

- Don't create additional threads that call Python APIs
- Use the existing timer system for periodic updates
- If you must use threads, ensure proper GIL handling

## Code Style Guidelines {#code-style}

When extending McRogueFace for your own projects, following these conventions will help maintain consistency:

### Naming Conventions

```cpp
// Class naming: UI prefix for UI components
class UIMyComponent : public UIDrawable {
    // Private members first
private:
    float my_property;
    
    // Then public interface
public:
    UIMyComponent();
    
    // Override virtual methods
    void render(sf::Vector2f pos, sf::RenderTarget& target) override;
};

// Python type naming: Py prefix
typedef struct {
    PyObject_HEAD
    std::shared_ptr<UIMyComponent> data;
} PyUIMyComponentObject;

// Namespace for type definitions
namespace mcrfpydef {
    static PyTypeObject PyUIMyComponentType = { ... };
}
```

### Documentation Best Practices

Every public method should have inline documentation:

```cpp
{"myMethod", (PyCFunction)UIMyComponent::myMethod, METH_VARARGS,
 "myMethod(arg1: float, arg2: int = 0) -> bool\n\n"
 "Brief description of what the method does.\n\n"
 "Args:\n"
 "    arg1: Description of first argument\n"
 "    arg2: Description of second argument (default: 0)\n\n"
 "Returns:\n"
 "    True if successful, False otherwise\n\n"
 "Example:\n"
 "    result = component.myMethod(1.5, 2)"},
```

### Testing Requirements

Create comprehensive tests:

```python
# tests/test_my_component.py
import mcrfpy
from mcrfpy import MyComponent
import sys

def test_basic_functionality():
    """Test basic component creation and properties"""
    comp = MyComponent(10, 20)
    assert comp.x == 10
    assert comp.y == 20
    
def test_edge_cases():
    """Test boundary conditions and error handling"""
    comp = MyComponent()
    comp.setProperty(-1)  # Should handle gracefully
    
def run_all_tests():
    test_basic_functionality()
    test_edge_cases()
    print("PASS: All tests completed successfully")
    sys.exit(0)

# Schedule tests to run after game loop starts
mcrfpy.setTimer("test", run_all_tests, 100)
```

## Conclusion

Extending McRogueFace with C++ opens up endless possibilities for enhancing your roguelike games. Whether you're adding particle effects, custom UI components, or integrating external libraries, the engine's architecture makes it straightforward to add new functionality while maintaining compatibility with the Python scripting layer.

Remember:
- Start small and test incrementally
- Follow the established patterns in the codebase
- Document your code thoroughly
- Share your extensions with the community!

Happy hacking! 🚀

---

*For more information, check out the [API Reference](/api-reference) and explore the [source code](https://github.com/jmccardle/McRogueFace).*

