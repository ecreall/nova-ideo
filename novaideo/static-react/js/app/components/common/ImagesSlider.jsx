import React from 'react';
import { withStyles } from 'material-ui/styles';
import ArrowBackIcon from 'material-ui-icons/ArrowBack';
import ArrowForwardIcon from 'material-ui-icons/ArrowForward';
import CloudDownloadIcon from 'material-ui-icons/CloudDownload';
import Button from 'material-ui/Button';
import classNames from 'classnames';
import * as Vibrant from 'node-vibrant';
import filesize from 'filesize';
import { Translate, I18n } from 'react-redux-i18n';

import OverlaidTooltip from './OverlaidTooltip';
import { getImagePalette, getFormattedDate } from '../../utils/globalFunctions';
import Dialog from './Dialog';
import UserAvatar from '../user/UserAvatar';

const styles = (theme) => {
  return {
    control: {
      backgroundColor: 'white',
      boxShadow: '0 1px 2px 0 rgba(0,0,0,.2)',
      color: '#2c2d30',
      opacity: 0.6,
      '&:hover': {
        opacity: 1,
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
      marginLeft: 'auto',
      marginRight: 'auto'
    },
    img: {
      margin: 'auto',
      maxHeight: 'calc(100vh - 144px)',
      maxWidth: 'calc(100vw - 120px)'
    },
    appBar: {
      backgroundColor: 'rgba(0, 0, 0, 0.35) !important',
      borderBottom: 'solid 1px rgba(255, 255, 255, 0.3)'
    },
    paper: {
      backgroundColor: 'rgba(0, 0, 0, 0.4)'
    },
    appBarContent: {
      color: 'white'
    },
    closeBtn: {
      color: 'white',
      '&::after': {
        display: 'block',
        position: 'absolute',
        top: '50%',
        right: 'auto',
        bottom: 'auto',
        left: 0,
        height: 20,
        transform: 'translateY(-50%)',
        borderRadius: 0,
        borderRight: '1px solid rgba(255, 255, 255, 0.5)',
        content: '""',
        color: '#2c2d30'
      }
    },
    headerContainer: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingRight: 10,
      color: 'white'
    },
    downLoadUrl: {
      color: 'white',
      lineHeight: 'normal'
    },
    downLoadIcon: {
      width: 30,
      height: 30
    },
    header: {
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'flex-start',
      margin: '0 10px',
      position: 'relative'
    },
    headerTitle: {
      fontSize: 15,
      color: 'white',
      fontWeight: 900,
      lineHeight: 'normal'
    },
    titleContainer: {
      display: 'flex'
    },
    headerAddOn: {
      color: '#d6d6d6',
      fontSize: 12,
      lineHeight: 'normal'
    },
    headerItem: {
      marginLeft: 5,
      fontWeight: 100,
      '&::before': {
        content: '""',
        background: '#d6d6d6',
        height: 8,
        width: 8,
        borderRadius: 5,
        display: 'inline-block',
        marginRight: 5
      }
    }
  };
};

const SliderHeader = ({ context, classes, image }) => {
  const author = context.author;
  return (
    <div className={classes.headerContainer}>
      <div className={classes.titleContainer}>
        <UserAvatar
          strictUrl={author.picture && author.picture.strictUrl}
          isAnonymous={author.isAnonymous}
          picture={author.picture}
          title={author.title}
        />
        <div className={classes.header}>
          <span className={classes.headerTitle}>
            {image.title}
          </span>
          <span className={classes.headerAddOn}>
            {author.title}
            {context.date &&
              <span className={classes.headerItem}>
                {getFormattedDate(context.date, 'date.format3')}
              </span>}
            <span className={classes.headerItem}>
              {context.title}
            </span>
          </span>
        </div>
      </div>
      <OverlaidTooltip
        tooltip={
          image.size
            ? <Translate value="common.imageSlider.downLoadImageSize" size={filesize(image.size)} />
            : I18n.t('common.imageSlider.downLoadImage')
        }
        placement="bottom"
      >
        <a className={classes.downLoadUrl} target="_blank" href={image.url}>
          <CloudDownloadIcon className={classes.downLoadIcon} />
        </a>
      </OverlaidTooltip>
    </div>
  );
};

class ImagesSlider extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      currentImage: props.current || 0,
      color: 'rgba(0, 0, 0, 0.4)'
    };
    this.setColor();
  }

  onNextClick = () => {
    const { currentImage } = this.state;
    const { images } = this.props;
    let next = currentImage + 1;
    next = next >= images.length ? 0 : next;
    this.setState({ currentImage: next }, this.setColor);
  };

  onPreviousClick = () => {
    const { currentImage } = this.state;
    const { images } = this.props;
    let previous = currentImage - 1;
    previous = previous < 0 ? images.length - 1 : previous;
    this.setState({ currentImage: previous }, this.setColor);
  };

  setColor = () => {
    const { images } = this.props;
    const { currentImage } = this.state;
    const image = images[currentImage];
    if (image) {
      getImagePalette(image.url).then((palette) => {
        const color = `rgba(${Vibrant.Util.hexToRgb(palette.DarkVibrant).join(',')}, 0.4)`;
        this.setState({ color: color });
      });
    }
  };

  render() {
    const { context, images, open, onClose, onOpen, classes } = this.props;
    const { currentImage, color } = this.state;
    const lengthImages = images.length;
    const image = images[currentImage];
    return (
      <Dialog
        appBar={<SliderHeader context={context} classes={classes} image={image} />}
        fullScreen
        open={open}
        onClose={onClose}
        onOpen={onOpen}
        classes={{
          paper: classes.paper,
          appBar: classes.appBar,
          appBarContent: classes.appBarContent,
          closeBtn: classes.closeBtn
        }}
        PaperProps={{ style: { backgroundColor: color } }}
      >
        {lengthImages > 1 &&
          <div>
            <Button
              onClick={this.onPreviousClick}
              variant="fab"
              aria-label="previous"
              className={classNames(classes.previous, classes.control)}
            >
              <ArrowBackIcon />
            </Button>
          </div>}
        <div className={classes.sliderContainer}>
          <img alt={image.name} className={classes.img} src={image.url} />
        </div>
        {lengthImages > 1 &&
          <div>
            <Button
              onClick={this.onNextClick}
              variant="fab"
              aria-label="next"
              className={classNames(classes.next, classes.control)}
            >
              <ArrowForwardIcon />
            </Button>
          </div>}
      </Dialog>
    );
  }
}

export default withStyles(styles, { withTheme: true })(ImagesSlider);