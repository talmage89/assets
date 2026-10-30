# One signature-motion GIF, rebuilt from the final GLB and accepted studio.
# Kept opt-in so normal docs regeneration never silently overwrites a reviewed GIF.
.PHONY: gif
gif: $(EXPORTS)
	$(PYTHON) ../common/gif.py --asset . --blender $(BLENDER)
