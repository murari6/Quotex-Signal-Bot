prompt = (
        f"Act as a strict Price Action Scalper. "
        f"The user wants to trade with {expiry} expiry. "
        f"Analyze the chart using this 4-step confirmation process:"
        f"\n1. MARKET STRUCTURE: Identify if the trend is Up, Down, or Ranging. "
        f"\n2. KEY LEVELS: Look for Support/Resistance lines or round numbers (e.g., 1.2000). "
        f"\n3. CANDLE PATTERNS: Look for rejection wicks, engulfing bars, or dojis."
        f"\n4. INDICATOR CONFIRMATION: If RSI or Moving Averages are visible, use them."
        f"\n\nDECISION RULE: Only generate a signal if at least 3 factors align. Otherwise, return 'NO TRADE'."
        f"\n\nOUTPUT FORMAT (JSON ONLY):"
        f"\nSIGNAL: [CALL / PUT / NO TRADE]"
        f"\nCONFIDENCE: [0-100%]"
        f"\nREASON: [List the 3 factors that confirmed this trade]"
    if uploaded_file:
        # Open the image
        raw_image = Image.open(uploaded_file)
        
        # 1. Convert to RGB to avoid format errors
        if raw_image.mode != 'RGB':
            raw_image = raw_image.convert('RGB')
            
        # 2. Increase Contrast (Helps AI see faint candle wicks)
        enhancer = ImageEnhance.Contrast(raw_image)
        image = enhancer.enhance(1.2) # Increase contrast by 20%
        
        # Display the SHARPENED image
        st.image(image, caption="Enhanced for AI Vision", use_container_width=True)
    )
