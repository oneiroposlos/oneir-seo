system_prompt_vi = (
    "Hoạt động như một chuyên gia phân loại văn bản cho nhiều ngôn ngữ.."
)

extract_mood_prompt_template_vi = (
    """
	Hoạt động như một chuyên gia phân loại văn bản. Phân tích thông tin đầu vào của người dùng bên dưới và làm theo các bước sau:
    1. **Xác định văn bản**: Phân loại tâm trạng chính của người dùng từ danh sách này:
       [Mua sắm, Branding, Tìm thông tin].
       Nếu không có tùy chọn nào phù hợp, hãy chọn tùy chọn gần nhất hoặc thêm một loại mới (ví dụ: "Sưu tầm").
    2. **Điểm tin cậy**: Đánh giá mức độ tin cậy của bạn vào phân loại (1-10, 10 = cao nhất).
    3. **Lý luận**: Giải thích các cụm từ chính, giọng điệu hoặc ngữ cảnh dẫn đến kết luận của bạn.
       Làm nổi bật các phép ẩn dụ, biểu tượng cảm xúc hoặc tín hiệu ngôn ngữ (ví dụ: mỉa mai).
    
    **User Input**: "{user_answering}"
    
    **Output Format**:
    - Category: [Detected text]
    - Confidence: [Score]/10
    - Reasoning: [1-2 câu]
    
    **Ví dụ**:
    1.
    User Input: "Mua nước mắm phú quốc ở đâu"
    Output:
    - Category: Mua sắm
    - Confidence: 9
    - Reasoning: Nguời dùng có nhu cầu tìm kiếm bằng việc "mua" một mặt hàng cụ thể là "nước mắm Phú Quốc".
    
    2.
    User Input: "nước mắm quảng trị"
    Output:
    - Category: Branding
    - Confidence: 10
    - Reasoning: Người dùng tìm kiếm chính xác hãng của sản phẩm.
    
    Bây giờ hãy phân tích và trả về thông tin theo định dạng có cấu trúc phù hợp với Model Python Pydantic sau:
    {format_instructions}
    """
)
