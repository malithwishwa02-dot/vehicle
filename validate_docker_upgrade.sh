#!/bin/bash
# ==============================================================================
# PROMETHEUS-CORE Docker Validation Script
# Validates Ubuntu 24.04 Docker upgrade implementation
# ==============================================================================

set -e

echo "================================================================"
echo "PROMETHEUS-CORE Docker Validation"
echo "================================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Validation function
validate() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
        exit 1
    fi
}

# 1. Check Docker installation
echo "[1/8] Checking Docker installation..."
docker --version > /dev/null 2>&1
validate "Docker is installed"

# 2. Check Docker Compose
echo "[2/8] Checking Docker Compose..."
docker compose version > /dev/null 2>&1
validate "Docker Compose is available"

# 3. Validate Dockerfile syntax
echo "[3/8] Validating Dockerfile syntax..."
test -f Dockerfile
validate "Dockerfile exists"

# 4. Validate docker-compose.yml
echo "[4/8] Validating docker-compose.yml..."
docker compose config --quiet
validate "docker-compose.yml syntax is valid"

# 5. Validate entrypoint.sh
echo "[5/8] Validating entrypoint.sh..."
test -f entrypoint.sh
bash -n entrypoint.sh
validate "entrypoint.sh syntax is valid"

# 6. Test Python platform detection
echo "[6/8] Testing platform detection..."
python3 -c "import platform; assert platform.system() in ['Linux', 'Windows'], 'Unsupported platform'" 2>/dev/null
validate "Platform detection works"

# 7. Test chronos module import
echo "[7/8] Testing chronos module import..."
python3 << 'EOF' > /dev/null 2>&1
import sys
sys.path.insert(0, '.')
from core.chronos import Chronos
chronos = Chronos()
assert chronos.platform in ['Linux', 'Windows']
EOF
validate "Chronos module imports correctly"

# 8. Test ChronosLinux with mock environment
echo "[8/8] Testing ChronosLinux with mock FAKETIME..."
FAKETIME="-90d" LD_PRELOAD="/usr/local/lib/faketime/libfaketime.so.1" python3 << 'EOF' > /dev/null 2>&1
import sys
import os
sys.path.insert(0, '.')
os.environ['FAKETIME'] = '-90d'
os.environ['LD_PRELOAD'] = '/usr/local/lib/faketime/libfaketime.so.1'
from core.chronos import Chronos
chronos = Chronos()
result = chronos.shift_time(90)
assert result == True, "Time shift verification failed"
EOF
validate "ChronosLinux verification works with FAKETIME"

echo ""
echo "================================================================"
echo -e "${GREEN}All validation checks passed!${NC}"
echo "================================================================"
echo ""
echo "Next steps:"
echo "  1. Build Docker image:     docker compose build"
echo "  2. Start services:         docker compose up -d"
echo "  3. View logs:              docker compose logs -f prometheus-core"
echo "  4. Run aging operation:    docker compose run --rm prometheus-core python level9_operations.py --age 90"
echo ""
