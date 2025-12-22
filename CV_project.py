import streamlit as st
import numpy as np
import cv2
from PIL import Image

def main():
    st.title("Image Processing with OpenCV and Streamlit")
   
    # Upload image
    uploaded_file = st.file_uploader(r'C:\Users\pandu\cv project', type=["jpg", "jpeg", "png"])
   
    if uploaded_file is not None:
        # Read the image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image',  use_container_width=True)

        # Convert to numpy array
        img_array = np.array(image)

        # Convert to grayscale using OpenCV
        gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        # Display grayscale image
        st.image(gray_image, caption='Grayscale Image',  use_container_width=True, channels="GRAY")
        
        # 1. BGR
        color_1=cv2.cvtColor(img_array,cv2.COLOR_BGR2BGRA)
        st.image(color_1,caption="BGR Image",use_container_width=True)
        
        #2. RGB 
        color_2=cv2.cvtColor(img_array, cv2.COLOR_RGB2RGBA)
        st.image(color_2,caption="RGB Image",use_container_width=True)
        
        # 3. RGBA
        color_3=cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGRA)
        st.image(color_3,caption="RGBA Image",use_container_width=True)
        
        # 4. BGRA
        bgra = cv2.cvtColor(img_array, cv2.COLOR_BGR2BGRA)
        st.image(bgra, caption="4. BGRA", use_container_width=True)
        
        # 6. HSV
        hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2HSV)
        st.image(hsv, caption="6. HSV", use_container_width=True)
        
        # 7. HLS
        hls = cv2.cvtColor(img_array, cv2.COLOR_BGR2HLS)
        st.image(hls, caption="7. HLS", use_container_width=True)
        
        # 8. LAB
        lab = cv2.cvtColor(img_array, cv2.COLOR_BGR2LAB)
        st.image(lab, caption="8. LAB", use_container_width=True)
        
        # 9. LUV
        luv = cv2.cvtColor(img_array, cv2.COLOR_BGR2LUV)
        st.image(luv, caption="9. LUV", use_container_width=True)

        # 10. YCrCb
        ycrcb = cv2.cvtColor(img_array, cv2.COLOR_BGR2YCrCb)
        st.image(ycrcb, caption="10. YCrCb", use_container_width=True)
        
        # 11. XYZ
        xyz = cv2.cvtColor(img_array, cv2.COLOR_BGR2XYZ)
        st.image(xyz, caption="11. XYZ", use_container_width=True)

        # 12. BGR to RGB (again for clarity)
        rgb_again = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        st.image(rgb_again, caption="12. BGR → RGB", use_container_width=True)

        # 13. RGB to BGR
        bgr_again = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        st.image(bgr_again, caption="13. RGB → BGR", use_container_width=True)

        # 14. HSV to BGR
        hsv_to_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        st.image(hsv_to_bgr, caption="14. HSV → BGR", use_container_width=True)

        # 15. LAB to BGR
        lab_to_bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        st.image(lab_to_bgr, caption="15. LAB → BGR", use_container_width=True)
        
        # 16. LUV to BGR
        luv_to_bgr = cv2.cvtColor(luv, cv2.COLOR_LUV2BGR)
        st.image(luv_to_bgr, caption="16. LUV → BGR", use_container_width=True)

        # 17. YCrCb to BGR
        ycrcb_to_bgr = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
        st.image(ycrcb_to_bgr, caption="17. YCrCb → BGR", use_container_width=True)

        # 18. XYZ to BGR
        xyz_to_bgr = cv2.cvtColor(xyz, cv2.COLOR_XYZ2BGR)
        st.image(xyz_to_bgr, caption="18. XYZ → BGR", use_container_width=True)

        # 19. RGB to GRAY
        gray_rgb = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        st.image(gray_rgb, caption="19. RGB → Grayscale", use_container_width=True, channels="GRAY")

        # 20. BGR to GRAY
        gray_bgr = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        st.image(gray_bgr, caption="20. BGR → Grayscale", use_container_width=True, channels="GRAY")
        
        # 21. AUTUMN 
        autumn = cv2.applyColorMap(gray_bgr, cv2.COLORMAP_AUTUMN)
        st.image(autumn, caption="AUTUMN", use_container_width=True)
        
        # 22. BONE
        bone = cv2.applyColorMap(gray_bgr, cv2.COLORMAP_BONE)
        st.image(bone, caption="BONE", use_container_width=True)
        
        # 23. JET
        jet = cv2.applyColorMap(img_array, cv2.COLORMAP_JET)
        st.image(jet, caption="JET", use_container_width=True)
        
        #24. WINTER
        winter = cv2.applyColorMap(img_array, cv2.COLORMAP_WINTER)
        st.image(winter, caption="WINTER", use_container_width=True)
        
        # 25. RAINBOW
        rainbow = cv2.applyColorMap(img_array, cv2.COLORMAP_RAINBOW)
        st.image(rainbow, caption="RAINBOW", use_container_width=True)
        
        # 26. OCEAN
        ocean = cv2.applyColorMap(img_array, cv2.COLORMAP_OCEAN)
        st.image(ocean, caption="OCEAN", use_container_width=True)
        
        # 27. SUMMER
        summer = cv2.applyColorMap(img_array, cv2.COLORMAP_SUMMER)
        st.image(summer, caption="SUMMER", use_container_width=True)
        
        # 28. SPRING
        spring = cv2.applyColorMap(img_array, cv2.COLORMAP_SPRING)
        st.image(spring, caption="SPRING", use_container_width=True)

        # 29. COOL
        cool = cv2.applyColorMap(img_array, cv2.COLORMAP_COOL)
        st.image(cool, caption="COOL", use_container_width=True)
        
        # 30. PINK
        pink = cv2.applyColorMap(img_array, cv2.COLORMAP_PINK)
        st.image(pink, caption="PINK", use_container_width=True)

        # 31. HOT
        hot = cv2.applyColorMap(img_array, cv2.COLORMAP_HOT)
        st.image(hot, caption="HOT", use_container_width=True)
        
        # 32. PARULA
        parula= cv2.applyColorMap(img_array, cv2.COLORMAP_PARULA)
        st.image(parula, caption="PARULA", use_container_width=True)
        
        # 33. MAGMA
        magma= cv2.applyColorMap(img_array, cv2.COLORMAP_MAGMA)
        st.image(magma, caption="MAGMA", use_container_width=True)

        # 34. INFERNO
        inferno = cv2.applyColorMap(img_array, cv2.COLORMAP_INFERNO)
        st.image(inferno, caption="INFERNO", use_container_width=True)
        
        # 35. PLASMA
        plasma = cv2.applyColorMap(img_array, cv2.COLORMAP_PLASMA)
        st.image(plasma, caption="PLASMA", use_container_width=True)
  
        # 36. VIRIDIS
        viridis= cv2.applyColorMap(img_array, cv2.COLORMAP_VIRIDIS)
        st.image(viridis, caption="VIRIDIS", use_container_width=True)

        # 37. CIVIDIS
        cividis = cv2.applyColorMap(img_array, cv2.COLORMAP_CIVIDIS)
        st.image(cividis, caption="CIVIDIS", use_container_width=True)

        # 38. TWILIGHT
        twilight = cv2.applyColorMap(img_array, cv2.COLORMAP_TWILIGHT)
        st.image(twilight, caption="TWILIGHT", use_container_width=True)

        # 39. TURBO
        turbo= cv2.applyColorMap(img_array, cv2.COLORMAP_TURBO)
        st.image(turbo, caption="TURBO", use_container_width=True)

        # 40. BGR COLOR
        color_deepgreen = cv2.applyColorMap(img_array, cv2.COLORMAP_DEEPGREEN)
        st.image(color_deepgreen, caption="DEEPGREEN COLOR", use_container_width=True)


    
    
if __name__ == "__main__":
    main()