/* eslint-disable react/no-array-index-key */
import React from 'react';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

import ImagesSlider from './ImagesSlider';

const styles = {
  imagesContainer: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'start',
    marginTop: 10,
    marginBottom: 10
  },
  itemsContainer: {
    display: 'flex',
    flexDirection: 'row',
    width: '100%'
  },
  images: {
    borderRadius: 3,
    backgroundColor: 'black',
    width: '100%'
  },
  imgBag: {
    backgroundColor: 'rgba(0, 0, 0, 0)',
    backgroundRepeat: 'no-repeat',
    backgroundAttachment: 'scroll',
    backgroundPositionX: 'center',
    backgroundPositionY: 'center',
    backgroundSize: 'cover',
    cursor: 'pointer'
  },
  firstItem: {
    width: '100%',
    paddingTop: '100%',
    borderRadius: 15,
    borderWidth: 0.5,
    borderColor: '#d6d7da',
    borderStyle: 'solid'
  },
  otherItem: {
    width: '100%',
    paddingTop: '100%',
    marginBottom: 2,
    borderRadius: 7,
    borderWidth: 0.5,
    borderColor: '#d6d7da',
    borderStyle: 'solid'
  },
  otherItemsContainer: {
    width: '20%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginLeft: 2
  },
  globalItemContainer: {
    width: '100%'
  },
  firstItemContainer: {
    width: '80%'
  },
  button: {
    boxShadow: '0px 1px 5px 0px rgba(0, 0, 0, 0.2), 0px 2px 2px 0px rgba(0, 0, 0, 0.14), 0px 3px 1px -2px rgba(0, 0, 0, 0.12)',
    marginTop: 5
  },
  plusItem: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff'
  }
};

export class DumbImagesPreview extends React.Component {
  state = {
    sliderOpen: false,
    current: 0
  };

  handleClose = () => {
    this.setState({ sliderOpen: false, current: 0 });
  };

  onClick = (index) => {
    this.setState({ sliderOpen: true, current: index });
  };

  renderItem = ({
    image, key, width, className
  }) => {
    const { classes } = this.props;
    return (
      <div
        onClick={() => {
          this.onClick(key || 0);
        }}
        key={key}
        style={{ backgroundImage: `url("${image.url}${image.variations.includes(width) ? width : ''}")` }}
        className={classNames(className, classes.imgBag)}
      />
    );
  };

  render() {
    const { images, context, classes } = this.props;
    if (images.length === 0) return <div />;
    const firstImage = images[0];
    const otherImagesToPreview = 3;
    const limit = images.length >= otherImagesToPreview ? otherImagesToPreview : images.length;
    const otherImages = images.length > 1 ? images.slice(1, limit) : [];
    const nbHiddenImages = limit === otherImagesToPreview ? images.length - otherImagesToPreview : 0;
    const { sliderOpen, current } = this.state;
    return (
      <div className={classes.imagesContainer}>
        <div className={classes.itemsContainer}>
          <div className={otherImages.length > 0 ? classes.firstItemContainer : classes.globalItemContainer}>
            {this.renderItem({ image: firstImage, width: 'big', className: classes.firstItem })}
          </div>
          {otherImages.length > 0 && (
            <div className={classes.otherItemsContainer}>
              {otherImages.map((image, key) => {
                return this.renderItem({
                  image: image,
                  key: key + 1,
                  width: 'small',
                  className: classes.otherItem
                });
              })}
              {nbHiddenImages ? (
                <Button
                  variant="fab"
                  color="primary"
                  aria-label="Add"
                  onClick={() => {
                    this.onClick(otherImagesToPreview);
                  }}
                  className={classes.button}
                >
                  <span className={classes.plusItem}>{`+${nbHiddenImages}`}</span>
                </Button>
              ) : null}
            </div>
          )}
        </div>
        {sliderOpen && (
          <ImagesSlider context={context} onClose={this.handleClose} open={sliderOpen} images={images} current={current} />
        )}
      </div>
    );
  }
}

export default withStyles(styles)(DumbImagesPreview);