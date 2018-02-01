import React from 'react';
import { withStyles } from 'material-ui/styles';
import ArrowBackIcon from 'material-ui-icons/ArrowBack';
import ArrowForwardIcon from 'material-ui-icons/ArrowForward';
import Slider from 'react-slick';
import Button from 'material-ui/Button';
import classNames from 'classnames';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

import Dialog from './Dialog';

const styles = (theme) => {
  return {
    control: {
      backgroundColor: 'white',
      boxShadow: '0 1px 2px 0 rgba(0,0,0,.2)',
      color: '#2c2d30',
      '&:hover': {
        backgroundColor: 'white',
        color: theme.palette.primary['500']
      }
    },
    previous: {
      marginLeft: 10
    },
    next: {
      marginRight: 10
    },
    sliderContainer: {
      maxWidth: 'calc(100vh - 120px)',
      margin: 'auto'
    },
    imgContainer: {
      minWidth: '50vh !important',
      minHeight: '50vh !important'
    },
    img: {
      maxHeight: 'calc(100vh - 150px)',
      maxWidth: '100%',
      margin: 'auto'
    }
  };
};

class ImagesSlider extends React.Component {
  constructor(props) {
    super(props);
    this.slider = null;
  }

  onNextClick = () => {
    this.slider.slickNext();
  };

  onPreviousClick = () => {
    this.slider.slickPrev();
  };

  renderItem = (image, key) => {
    const { classes } = this.props;
    return (
      <div className={classes.imgContainer} key={key}>
        <img alt={image.name} className={classes.img} src={image.url} />
      </div>
    );
  };

  render() {
    const { classes, images, open, current, onClose, onOpen } = this.props;
    const settings = {
      fade: true,
      adaptiveHeight: true,
      centerMode: true,
      slidesToShow: 1,
      slidesToScroll: 1,
      slickGoTo: current
    };
    const lengthImages = images.length;
    return (
      <Dialog appBar="Images" fullScreen open={open} onClose={onClose} onOpen={onOpen}>
        {lengthImages > 1 &&
          <div>
            <Button
              onClick={this.onPreviousClick}
              fab
              aria-label="previous"
              className={classNames(classes.previous, classes.control)}
            >
              <ArrowBackIcon />
            </Button>
          </div>}
        <div className={classes.sliderContainer}>
          <Slider
            ref={(slider) => {
              this.slider = slider;
            }}
            {...settings}
          >
            {images.map((image, key) => {
              return this.renderItem(image, key);
            })}
          </Slider>
        </div>
        {lengthImages > 1 &&
          <div>
            <Button onClick={this.onNextClick} fab aria-label="next" className={classNames(classes.next, classes.control)}>
              <ArrowForwardIcon />
            </Button>
          </div>}
      </Dialog>
    );
  }
}

export default withStyles(styles, { withTheme: true })(ImagesSlider);