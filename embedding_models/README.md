# CÁC MÔ HÌNH EMBEDDING

Các mô hình embedding giúp biểu diễn văn bản dưới dạng các vector nhiều chiều, nhằm đảm bảo hiệu quả tính toán và giữ được ngữ nghĩa của văn bản. Có nhiều loại mô hình Embedding khác nhau, tùy quy mô dự án để chọn ra những mô hình embedding phù hợp. Đối với dự án "Xây dựng chatbot hỗ trợ học lịch sử Việt Nam" chủ yếu phục vụ nhu cầu của người Việt, vì thế các mô hình embedding được sử dụng trong dự án này tập trung vào các mô hình embedding chuyên biệt cho tiếng Việt, nhẹ nhưng vẫn đảm bảo kết quả chính xác.

# MỘT SỐ MÔ HÌNH EMBEDDING THAM KHẢO

Lưu ý: Để có thể clone các mô hình này về máy, hãy đảm bảo git-lfs đã được cài đặt (xem thêm tại: https://git-lfs.com)

```
git lfs install
```

## sentence-transformers/distiluse-base-multilingual-cased-v2

* Hỗ trợ đa ngôn ngữ (bao gồm cả tiếng Việt)
* Nhẹ
* Dựa trên DistiBERT

```
git clone https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v2
```

## bkai-foundation-models/vietnamese-bi-encoder

* Bi-encoder nhẹ cho tiếng Việt
* Phù hợp với nhiệm vụ semantic search
* Mô hình nhỏ, nhanh. Có thể chạy trên CPU

```
git clone https://huggingface.co/bkai-foundation-models/vietnamese-bi-encoder
```

## intfloat/multilingual-e5-small

* Được tối ưu cho nhiệm vụ retrieval (semantic search)
* Hiệu quả cao
* Hỗ trợ tiếng Việt
* Có thể sử dụng trên CPU

```
git clone https://huggingface.co/intfloat/multilingual-e5-small
```

## VoVanPhuc/sup-SimCSE-VietNamese-phobert-base

* Được tối ưu cho tiếng Việt
* Fine-tuned theo SimCSE (Contrastive Learning)

```
git clone https://huggingface.co/VoVanPhuc/sup-SimCSE-VietNamese-phobert-base
```

## dangvantuan/vietnamese-embedding

* Được tối ưu cho tiếng Việt
* Nhẹ
* Hiệu quả cao

```
git clone https://huggingface.co/dangvantuan/vietnamese-embedding
```

## sentence-transformers/all-MiniLM-L6-v2

- Hoạt động tốt trên tài liệu tiếng Anh

```
git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
```
