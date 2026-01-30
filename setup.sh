#!/bin/bash

# Quick Setup Script for Data Analytics Project
# This script helps you set up the project quickly

echo "  Data Analytics Project - Quick Setup"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment"
    exit 1
fi

echo "Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies"
    exit 1
fi

echo "Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file and add your NewsAPI key"
else
    echo ".env file already exists"
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your NewsAPI key"
echo "   Get one free at: https://newsapi.org/"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the project:"
echo "   python main.py"
echo ""
echo "For more info, see README.md"
echo ""
