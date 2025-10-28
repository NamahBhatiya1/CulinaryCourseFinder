# Culinary Course Selector

## Overview

This is a Streamlit-based web application designed to help users explore and select culinary courses. The application provides an interactive interface for browsing culinary education paths and maintaining favorites. The system is built with Python and Streamlit, featuring a modern dark purple/black theme with responsive design supporting mobile, tablet, and desktop devices.

**Latest Update (October 28, 2025)**: 
- Filter persistence now fully implemented using URL query parameters - all filters save across page navigation
- Performance optimizations for lower-end devices: removed CSS animations, gradients, and transform effects
- App is cellular data friendly with zero external resource dependencies

## User Preferences

Preferred communication style: Simple, everyday language.

## Performance & Optimization

**Cellular Data Usage**: ✅ **MINIMAL - Cellular Data Friendly**
- **No external API calls** - All data is hardcoded locally
- **No external images** - Only emoji icons (Unicode characters)
- **No external CSS/JS libraries** - Pure Streamlit framework
- **No external fonts** - Uses system fonts
- **Data transfer**: Only initial app load (~200KB) + minimal WebSocket updates for state changes
- **Result**: App works efficiently on 3G/4G/5G networks with minimal data consumption

**Lower-End Device Optimizations**:
- Removed CSS gradients (replaced with solid colors for faster rendering)
- Removed transform animations (translateY effects on hover)
- Simplified box shadows (reduced blur and spread values)
- Removed transition effects to reduce GPU usage
- Optimized for devices with limited CPU/GPU capabilities
- Maintains full functionality and visual appeal while improving performance

## System Architecture

### Frontend Architecture

**Framework**: Streamlit (Python-based web framework)
- **Rationale**: Chosen for rapid application development without requiring JavaScript knowledge. Streamlit handles routing, state management, and UI rendering automatically.
- **Layout**: Wide layout mode (`layout="wide"`) for optimal content presentation
- **Pros**: Fast prototyping, Python-native development, minimal boilerplate code
- **Cons**: Limited customization compared to traditional web frameworks, server-side rendering only

**State Management**: Streamlit's `session_state`
- **Purpose**: Track user selections and favorites during active sessions
- **Implementation**: In-memory storage with optional PostgreSQL persistence
- **Rationale**: Provides immediate user experience while attempting database persistence

**Responsive Design**: Three-tier breakpoint system
- Desktop (>768px): Full-featured layout
- Tablet (≤768px): Optimized spacing and typography
- Mobile (≤480px): Single column, touch-friendly controls (48px minimum button height)

**Design System**:
- Dark theme with purple accents (solid color `#2D1B4E` for performance)
- High contrast white text (`#ffffff`) for accessibility
- Interactive elements with simple hover effects (no animations for performance)
- Orange CTAs (`#FF6B35`) for primary actions
- Optimized shadows (2-8px blur for fast rendering)

### Backend Architecture

**Application Structure**:
- `app.py`: Main Streamlit application entry point
- `main.py`: Alternative entry point (minimal "Hello World" implementation)
- Hybrid data layer combining session storage with optional database persistence

**Favorites System**: Resilient dual-storage architecture
- **Problem**: Need to persist user favorites while maintaining uptime even when database is unavailable
- **Solution**: Graceful degradation pattern that attempts PostgreSQL persistence but falls back to session storage
- **Implementation**:
  1. Check for `DATABASE_URL` environment variable
  2. Attempt database connection and write operation
  3. On failure, warn user once per session and store in `session_state`
  4. Always update session state as source of truth for current session
- **Pros**: Application remains functional during database outages, user experience preserved
- **Cons**: Session-only storage is ephemeral and lost on page refresh when database unavailable

**Data Operations**:
- `add_favorite(item_type, item_name)`: Dual-write to database and session state
- `remove_favorite(item_type, item_name)`: Function signature defined but implementation incomplete
- Uses `ON CONFLICT DO NOTHING` clause to prevent duplicate favorites

### External Dependencies

**Database**: PostgreSQL
- **Connection**: psycopg2 driver via `DATABASE_URL` environment variable
- **Schema**: `favorites` table with columns:
  - `user_id` (currently hardcoded as 'default_user')
  - `item_type` (categorizes favorite items)
  - `item_name` (stores the item identifier)
  - Constraint: Unique combination to prevent duplicates
- **Rationale**: PostgreSQL chosen for relational data storage with ACID guarantees
- **Note**: Database is optional dependency; application functions without it

**Python Libraries**:
- `streamlit`: Core web framework for UI
- `pandas`: Data manipulation (imported but usage not evident in provided code)
- `psycopg2`: PostgreSQL database adapter
- `os`: Environment variable access for configuration

**Configuration**:
- Environment-based configuration via `DATABASE_URL`
- No hardcoded credentials or connection strings
- Graceful handling of missing environment variables

### Filter Persistence System

**Implementation**: URL Query Parameters + Session State
- **Course Selection**: Persists via `?course=CourseName` parameter
- **Budget Range**: Persists via `?budget_min=X&budget_max=Y` parameters  
- **Country Filter**: Persists via `?countries=USA,France` (comma-separated)
- **Rating Filter**: Persists via `?min_rating=4.5` parameter
- **Duration Filter**: Persists via `?durations=2+years,4+years` (comma-separated)
- **Search Query**: Persists via `?search=keyword` parameter

**Architecture**:
1. On page load, read query params and populate session state
2. Widgets use session state as default values
3. On widget change, update both session state AND query params
4. Filters persist across page navigation automatically via URL
5. Users can bookmark or share filtered views

**Benefits**:
- Filters survive page navigation
- Users can use browser back/forward buttons
- Shareable filtered views via URL
- Better user experience on return visits