use image::{GenericImageView, ImageBuffer, Rgb};
use std::io;
use std::f32;

fn main() {

    //Read inputs
    //image path
    let mut image_name = String::new();
    println!("Please enter the name or path of the image you want to edit");
    io::stdin()
        .read_line(&mut image_name)
        .expect("Failed to read line");
        image_name = image_name.trim().parse().unwrap();

    //user_color to use in recolor()
    let mut user_color: [u8;3] = [0,0,0];
    for i in 0..3{
        let mut val = String::new();
        println!("Please input color value {}",i+1);
        io::stdin()
        .read_line(&mut val)
        .expect("Failed to read line");

    user_color[i] = val.trim().parse().unwrap();
    }

    //choose if rotate should be normalized
    let mut gets_normalized = String::new();
    println!("Should your rotation matrix be normalized? (y/n)");
    io::stdin()
        .read_line(&mut gets_normalized)
        .expect("Failed to read line");
    gets_normalized = gets_normalized.trim().parse().unwrap();

    //get rotation matrix
    let mut user_rot: [[f32;2];2] = [[1.0,0.0],[0.0,1.0]];
    for i in 0..4{
        let mut val = String::new();
        println!("Please input rotation matrix value {} (Default:{})",i+1,user_rot[i/2][i%2]);
        io::stdin()
        .read_line(&mut val)
        .expect("Failed to read line");

    user_rot[i/2][i%2] = val.trim().parse().unwrap();
    }

    let width = 200 + 1;
    let height = 200 + 1;

    //load image, crop middle and transform to imagebuffer
    let mut img = image::open(image_name).unwrap();
    img = img.crop(img.width()/2 - width/2, img.height()/2 - height/2, width, height);
    
    //make image to imagebuffer
    let mut imgbuf = img.to_rgb8();

    //use functions defined below
    imgbuf = to_grayscale(imgbuf);

    imgbuf = recolor(imgbuf, user_color[0],user_color[1],user_color[2],width,height);

    if gets_normalized == "y"{
        imgbuf = rotate(imgbuf, user_rot[0][0],user_rot[0][1],user_rot[1][0],user_rot[1][1], width, height);
    } else {
        imgbuf = rotate_normalized(imgbuf, user_rot[0][0],user_rot[0][1],user_rot[1][0],user_rot[1][1], width, height);
    }
    

    // Save the image as "output.png", the format is deduced from the path
    imgbuf.save("output.png").unwrap();
}

//converts the image to grayscale using average lumination of each pixel
fn to_grayscale(mut buffer: ImageBuffer<Rgb<u8>, Vec<u8>>) -> ImageBuffer<Rgb<u8>, Vec<u8>>{

    for (_, _, pixel) in buffer.enumerate_pixels_mut() {
        //get the rgb value of a pixel
        let image::Rgb(data) = *pixel;
        //average the color values for every pixel
        let gray_tone = ((data[0] as f32 + data[1] as f32 + data[2] as f32) / 3 as f32) as u8;
        //and change the referenced value
        *pixel = image::Rgb([gray_tone,gray_tone,gray_tone]);
    }

    buffer
}

//recolors every second pixel in the image with rgb values as attributes
fn recolor(mut buffer: ImageBuffer<Rgb<u8>, Vec<u8>>,r: u8,g: u8,b: u8,w: u32,h: u32) -> ImageBuffer<Rgb<u8>, Vec<u8>>{

    let mut copybuffer = image::ImageBuffer::new(w,h);
    //alternate between copying a pixel and changing it's colorvalue
    for (x, y, pixel) in copybuffer.enumerate_pixels_mut() {
        if ((x+y) % 2) == 0 {
            *pixel = buffer.get_pixel_mut(x, y).clone();
        } else {
            *pixel = image::Rgb([r,g,b]);
        }
    }
    copybuffer
}

//rotates the image according to the input values
fn rotate(mut buffer: ImageBuffer<Rgb<u8>, Vec<u8>>,x1: f32,y1: f32,x2: f32,y2: f32,w: u32,h: u32) -> ImageBuffer<Rgb<u8>, Vec<u8>>{

    let mut copybuffer = image::ImageBuffer::new(w,h);

    for (x, y, pixel) in buffer.enumerate_pixels_mut() {
        //convert the coordinates so 0,0 is in the middle of the imagebuffer
        let x = (x as i32 - (w/2) as i32) as f32;
        let y = (y as i32 - (h/2) as i32) as f32;
        //get the new position by calculation the dotproduct of position vector and rotation matrix
        let newpos = [((x1*x+y1*y) + (w/2) as f32) as u32,((x2*x+y2*y) + (h/2) as f32) as u32];
        //copy pixelvalues to new position
        if newpos[0] < w  && newpos[1] < h {
            let newpixel = copybuffer.get_pixel_mut(newpos[0], newpos[1]);
            *newpixel = pixel.clone();
        }
    }
    //return rotated copy
    copybuffer
}
//rotates the image according to the normalized input values
fn rotate_normalized(mut buffer: ImageBuffer<Rgb<u8>, Vec<u8>>,x1: f32,y1: f32,x2: f32,y2: f32,w: u32,h: u32) -> ImageBuffer<Rgb<u8>, Vec<u8>>{

    let mut copybuffer = image::ImageBuffer::new(w,h);

    for (x, y, pixel) in buffer.enumerate_pixels_mut() {
        //convert the coordinates so 0,0 is in the middle of the imagebuffer
        let x = x as f32 - (w/2) as f32;
        let y = y as f32 - (h/2) as f32;
        //get the absolute value of the two vectors in the rotation matrix
        let absv1 = (x1*x1+y1*y1).sqrt();
        let absv2 = (x2*x2+y2*y2).sqrt();
        //normalize those vectors
        let normalized_rotation = [[x1/absv1,y1/absv1],[x2/absv2,y2/absv2]];

        //get the new position by calculation the dotproduct of normalized position vector and rotation matrix
        let newpos = [(normalized_rotation[0][0] * x + normalized_rotation[0][1]*y + (w/2) as f32) as u32,(normalized_rotation[1][0]*x +normalized_rotation[1][1]*y + (h/2) as f32) as u32];

        //copy pixelvalues to new position
        if newpos[0] < w  && newpos[1] < h {
            let newpixel = copybuffer.get_pixel_mut(newpos[0], newpos[1]);
            *newpixel = pixel.clone();
        }

    }
    copybuffer
}