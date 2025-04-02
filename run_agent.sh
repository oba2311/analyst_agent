#!/bin/bash
# Run the Marketing Analyst Agent with convenient options

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Parse arguments
QUERY=""
MODEL=""
VERBOSE=false
NO_TRACING=false
HIGHLIGHT=""
INTERACTIVE=false

# Process arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -q|--query)
            QUERY="$2"
            shift 2
            ;;
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -n|--no-tracing)
            NO_TRACING=true
            shift
            ;;
        -h|--highlight)
            # Collect all highlight terms until next option
            while [[ "$2" != "" && ! "$2" =~ ^- ]]; do
                HIGHLIGHT="$HIGHLIGHT \"$2\""
                shift
            done
            shift
            ;;
        -i|--interactive)
            INTERACTIVE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: ./run_agent.sh [-q|--query QUERY] [-m|--model MODEL] [-v|--verbose] [-n|--no-tracing] [-h|--highlight TERMS...] [-i|--interactive]"
            exit 1
            ;;
    esac
done

# Build command
CMD="python3 -m src.main"

if [ ! -z "$MODEL" ]; then
    CMD="$CMD --model $MODEL"
fi

if [ "$VERBOSE" = true ]; then
    CMD="$CMD --verbose"
fi

if [ "$NO_TRACING" = true ]; then
    CMD="$CMD --no-tracing"
fi

if [ ! -z "$HIGHLIGHT" ]; then
    CMD="$CMD --highlight $HIGHLIGHT"
fi

if [ ! -z "$QUERY" ]; then
    CMD="$CMD --query \"$QUERY\""
elif [ "$INTERACTIVE" = true ]; then
    # No query argument needed for interactive mode
    echo "Starting in interactive mode..."
else
    # Default to interactive mode if no query and not explicitly set
    echo "No query provided, starting in interactive mode..."
fi

# Run the command
echo "Running: $CMD"
eval $CMD

# Deactivate virtual environment
deactivate 