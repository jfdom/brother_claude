#!/bin/bash
# Setup Brother Claude alias that always works

# Remove any existing brother-claude aliases
sed -i '/brother-claude/d' ~/.bashrc
if [ -f ~/.zshrc ]; then
    sed -i '/brother-claude/d' ~/.zshrc  
fi

# Create internal symlink within Brother Claude folder
ln -sf "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/BOOTING COMMAND/SCRIPTS/brother-claude-absolute" "/home/agat/symbolic_spine_work/The Symbolic Spine/ROOT/BROTHER CLAUDE/brother-claude"

# Create fresh alias that uses internal symlink with escaped spaces
echo "# Brother Claude Auto-Awakening Alias - $(date)" >> ~/.bashrc
echo "alias brother-claude=\"/home/agat/symbolic_spine_work/The\\\ Symbolic\\\ Spine/ROOT/BROTHER\\\ CLAUDE/brother-claude\"" >> ~/.bashrc

# Also add to zshrc if it exists
if [ -f ~/.zshrc ]; then
    echo "# Brother Claude Auto-Awakening Alias - $(date)" >> ~/.zshrc  
    echo "alias brother-claude=\"/home/agat/symbolic_spine_work/The\\\ Symbolic\\\ Spine/ROOT/BROTHER\\\ CLAUDE/brother-claude\"" >> ~/.zshrc
fi

echo "Brother Claude alias setup complete!"
echo "Restart your terminal or run: source ~/.bashrc"
echo "Then type: brother-claude"