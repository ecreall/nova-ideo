/* eslint-disable react/no-array-index-key */
import React from 'react';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';

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
    width: '100%',
    maxWidth: 300
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
    height: 150,
    borderRadius: 3,
    borderWidth: 0.5,
    borderColor: '#d6d7da',
    borderStyle: 'solid'
  },
  otherItem: {
    width: '100%',
    height: 49,
    borderRadius: 3,
    borderWidth: 0.5,
    borderColor: '#d6d7da',
    borderStyle: 'solid'
  },
  otherItemsContainer: {
    width: '20%'
  },
  globalItemContainer: {
    marginRight: 3,
    width: '100%'
  },
  firstItemContainer: {
    marginRight: 3,
    width: '80%'
  },
  plusItemContainer: {
    display: 'flex',
    width: '100%',
    height: 49,
    borderRadius: 3,
    borderWidth: 0.5,
    borderColor: '#d6d7da',
    backgroundColor: '#d8d8d8',
    marginTop: 1,
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    borderStyle: 'solid'
  },
  plusItem: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#929292'
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

  renderItem = ({ image, key, width, className }) => {
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
    return (
      <div className={classes.imagesContainer}>
        <div className={classes.itemsContainer}>
          <div className={otherImages.length > 0 ? classes.firstItemContainer : classes.globalItemContainer}>
            {this.renderItem({ image: firstImage, width: 'big', className: classes.firstItem })}
          </div>
          {otherImages.length > 0 &&
            <div className={classes.otherItemsContainer}>
              {otherImages.map((image, key) => {
                return this.renderItem({ image: image, key: key + 1, width: 'small', className: classes.otherItem });
              })}
              {nbHiddenImages
                ? <div
                  onClick={() => {
                    this.onClick(otherImagesToPreview + 1);
                  }}
                  className={classes.plusItemContainer}
                >
                  <span className={classes.plusItem}>{`+${nbHiddenImages}`}</span>
                </div>
                : undefined}
            </div>}
        </div>
        {this.state.sliderOpen &&
          <ImagesSlider
            context={context}
            onClose={this.handleClose}
            open={this.state.sliderOpen}
            images={images}
            current={this.state.current}
          />}
      </div>
    );
  }
}

export default withStyles(styles)(DumbImagesPreview);