void yuv2rgb_semi(unsigned char* yimg, unsigned short* uv, unsigned char* out, int width, int height)
{
    int y,v,u, r, g, b;
    unsigned char *image = out;

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            y = (*yimg);
            u = ((*uv & 0xff00) >> 8);
            v = (*uv & 0xff);
            b = (int) (y + 1.773 * (u-128));
            g = (int) (y - 0.714 * (v-128) - 0.344 * (u-128));
            r = (int) (y + 1.403 * (v-128));
            if (r < 0) r = 0;
            if (r > 255) r = 255;
            if (g < 0) g = 0;
            if (g > 255) g = 255;
            if (b < 0) b = 0;
            if (b > 255) b = 255;

            *(image++) = r;
            *(image++) = g;
            *(image++) = b;

            yimg++;
            if(j%2 != 0){
                uv++;
            }
        }
        if (i%2 == 0) {
            uv -= width / 2;
        }
    }
}

