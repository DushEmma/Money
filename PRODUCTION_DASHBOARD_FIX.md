# Production Dashboard 500 Error Fix

## Problem
Users could register and login successfully, but when accessing the dashboard in production, they received a **500 Internal Server Error**.

## Root Causes
1. **Missing database columns** - The production database was missing Worker table columns that were added later:
   - `id_photo`
   - `experience_details`
   - `reference_name`
   - `reference_phone`
   - `reference_relationship`
   - `national_id_number`

2. **Insufficient error handling** - The dashboard route did not handle missing columns gracefully
3. **Rigid profile completion check** - The `calculate_profile_completion()` function accessed columns without checking if they existed

## Solutions Implemented

### 1. Made Profile Completion Check Resilient
**File**: `app.py` - `calculate_profile_completion()` function
- Changed from direct attribute access to `getattr()` with default values
- Added try-catch wrapper with proper error logging
- Returns 0 on error instead of crashing

**Before**:
```python
if worker.id_photo:  # Crashes if column doesn't exist
    completion += 1
```

**After**:
```python
if getattr(worker, 'id_photo', None):  # Safe access with default None
    completion += 1
```

### 2. Enhanced Dashboard Route Error Handling
**File**: `app.py` - `/dashboard` route
- Wrapped profile completion check in separate try-catch
- Wrapped job recommendations fetch in try-catch
- Wrapped employer dashboard logic in comprehensive try-catch
- Each section has fallback values
- Detailed error logging for debugging

### 3. Automatic Database Column Migration
**File**: `ensure_worker_columns.py` (NEW)
- Checks for missing Worker table columns
- Automatically adds missing columns on startup
- Supports both SQLite (dev) and PostgreSQL (prod)
- Handles both databases' SQL syntax differences

### 4. Auto-Migration on App Startup
**File**: `app.py` - Added `run_migrations()` before_request hook
- Runs column migration automatically on first request
- Prevents 500 errors from missing columns

## Deployment Steps

### Option 1: Automatic (Recommended)
Simply push the updated code to production. The app will automatically:
1. Detect missing columns
2. Add them on the first request
3. Continue working normally

### Option 2: Manual Migration (Before Deployment)
If you want to run the migration before restarting the app:

```bash
python ensure_worker_columns.py
```

Then deploy the updated `app.py`.

### Option 3: One-Time Setup Script
```bash
# SSH into production server, then:
cd /path/to/umukozi
python ensure_worker_columns.py
# Verify output shows "✅ All required columns verified to exist!"
```

## Verification

### Check if the fix is working:

1. **In Production Logs**:
   - Look for: `✅ Worker column migration check completed at startup`
   - Or: `⚠️ Error running migration at startup:` (if there are issues)

2. **Test Dashboard**:
   - Create a test worker account
   - Register and login
   - Navigate to `/dashboard`
   - Should see the dashboard (not 500 error)

3. **Check Error Logs** (`logs/app.log`):
   ```bash
   tail -f logs/app.log | grep -E "migration|dashboard|Error"
   ```

## Files Modified

1. **app.py**
   - Enhanced `calculate_profile_completion()` function
   - Improved `/dashboard` route error handling
   - Added startup migration check

2. **ensure_worker_columns.py** (NEW)
   - Database migration script
   - Column existence verification
   - Support for multiple database types

## Rollback Plan

If issues occur:

1. The changes are backward compatible
2. Simply revert `app.py` to previous version
3. The database changes are additive (new columns) and don't break existing code

## Testing Checklist

- [ ] Worker can register successfully
- [ ] Worker can login successfully  
- [ ] Worker can access `/dashboard`
- [ ] Employer can access `/dashboard`
- [ ] Admin can access `/admin/dashboard`
- [ ] Check logs for migration messages
- [ ] No 500 errors on any dashboard

## Additional Notes

- The migration is **idempotent** - it's safe to run multiple times
- Missing columns are **non-critical** for basic functionality
- The app continues working even if migration fails (with graceful degradation)
- Future schema updates should follow the same pattern of using `getattr()` for optional columns

## Support

If the dashboard still shows 500 errors after deployment:

1. Check `logs/app.log` for the actual error
2. Verify database connection is working: `python -c "from models import db; print(db)"`
3. Check if Worker table exists: Check database directly
4. Run manual migration: `python ensure_worker_columns.py`
