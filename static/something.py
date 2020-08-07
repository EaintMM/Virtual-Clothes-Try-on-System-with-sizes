for obj in findRects:
                    print("Rectanlge corr is")
                    print(obj)
                    image = cv2.rectangle(image, (obj[0],obj[1]), (obj[0]+obj[2], obj[1]+obj[3]), (0, 255, 0), 2)
                    print(obj[2])
                    sprite = cv2.imread(image_path,-1)
                    scale_percent = 25 # percent of original size
                    width = int(sprite.shape[1] * scale_percent / 100)
                    height = int(sprite.shape[0] * scale_percent / 100)
                    dim = (width, height)
                    # resize image
                    resized = cv2.resize(sprite, dim, interpolation = cv2.INTER_AREA)
                    #sprite = rotate_bound(sprite, angle)
                    #draw_sprite(image,sprite,obj[0],obj[1])
                    draw_sprite(image,resized,obj[0],obj[3]-70)
                    #(x1,y1,w1,h1) = get_face_boundbox(shape, 6)
                    #apply_sprite(image,image_path,obj[0]+obj[2],obj[2],obj[3], 0)