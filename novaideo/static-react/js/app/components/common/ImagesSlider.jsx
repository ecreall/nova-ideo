import React from 'react';
import { withStyles } from 'material-ui/styles';
import Dialog from 'material-ui/Dialog';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import IconButton from 'material-ui/IconButton';
import Typography from 'material-ui/Typography';
import CloseIcon from 'material-ui-icons/Close';
import ArrowBackIcon from 'material-ui-icons/ArrowBack';
import ArrowForwardIcon from 'material-ui-icons/ArrowForward';
import Slide from 'material-ui/transitions/Slide';
import Slider from 'react-slick';
import Button from 'material-ui/Button';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%'
  },
  appBar: {
    position: 'relative',
    backgroundColor: '#fff',
    boxShadow: '0 1px 0 rgba(0,0,0,.1)'
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
  img: {
    maxHeight: 'calc(100vh - 150px)',
    maxWidth: '100%',
    margin: 'auto'
  },
  paper: {
    backgroundColor: '#f3f3f3'
  },
  flex: {
    flex: 1
  }
};

function Transition(props) {
  return <Slide direction="up" {...props} />;
}

class ImagesSlider extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      entered: false
    };
    this.slider = null;
  }
  componentDidMount() {
    setTimeout(() => {
      window.dispatchEvent(new Event('resize'));
    }, 0);
  }
  onEntered = () => {
    this.setState({ entered: true });
  };

  onClose = () => {
    this.setState({ entered: false }, this.props.onClose);
  };

  onNextClick = () => {
    this.slider.slickNext();
  };

  onPreviousClick = () => {
    this.slider.slickPrev();
  };

  render() {
    const { classes, images, open, current } = this.props;
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
      <Dialog
        classes={{ paper: classes.paper }}
        onEntered={this.onEntered}
        fullScreen
        open={open}
        onClose={this.onClose}
        transition={Transition}
      >
        <AppBar className={classes.appBar}>
          <Toolbar>
            <Typography type="title" color="primary" className={classes.flex}>
              Sound
            </Typography>
            <IconButton color="primary" onClick={this.onClose} aria-label="Close">
              <CloseIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
        {this.state.entered &&
          <div className={classes.container}>
            {lengthImages > 1 &&
              <div>
                <Button onClick={this.onPreviousClick} fab aria-label="previous" className={classes.previous}>
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
                  return (
                    <div style={{ minWidth: '50vh', minHeight: '50vh' }} key={key}>
                      <img alt={image.name} className={classes.img} src={image.url} />
                    </div>
                  );
                })}
              </Slider>
            </div>
            {lengthImages > 1 &&
              <div>
                <Button onClick={this.onNextClick} fab aria-label="next" className={classes.next}>
                  <ArrowForwardIcon />
                </Button>
              </div>}
          </div>}
      </Dialog>
    );
  }
}

export default withStyles(styles)(ImagesSlider);