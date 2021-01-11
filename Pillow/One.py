from PIL import Image, ImageFilter
import os


# image1 = Image.open('resume.jpg')
# image1.show()
# image1.save('pngs/hi.jpg')

# for f in os.listdir('.'):
#     if f.endswith('.jpg'):
#         # print(f)
#         i = Image.open(f)
#         # i.show()
#         fn, fext = os.path.splitext(f)
#         # print(fn,fext)
#         i.save(f'pngs/{fn}.png')

max = (300,300)
# for f in os.listdir('.'):
#     if f.endswith('.jpg'):
#         i = Image.open(f) # make f into an image object
#         fn, fext = os.path.splitext(f)
#         i.thumbnail(max)
#         i.save(f'300/{fn}_300.{fext}')

# image2 = Image.open('hi.png')
# image2.rotate(90).show()
# image2.convert(mode='L').show() #  ratating # look in documentation
# image2.filter(ImageFilter.GaussianBlur(15)).show() # blurring

