/* eslint-disable react/no-array-index-key */
import React from 'react';

const styles = {
  imagesContainer: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 10,
    paddingRight: 10
  },
  itemsContainer: {
    display: 'flex',
    flexDirection: 'row',
    width: '100%',
    maxWidth: 400
  },
  images: {
    borderRadius: 3,
    backgroundColor: 'black',
    width: '100%'
  },
  firstItem: {
    width: '100%',
    height: 200,
    borderRadius: 3,
    borderWidth: 0.5,
    borderColor: '#d6d7da'
  },
  otherItem: {
    width: '100%',
    height: 50,
    borderRadius: 3,
    marginTop: 2,
    borderWidth: 0.5,
    borderColor: '#d6d7da'
  },
  otherItemsContainer: {
    width: '19%'
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
    height: 50,
    borderRadius: 3,
    borderWidth: 0.5,
    borderColor: '#d6d7da',
    backgroundColor: '#d8d8d8',
    marginTop: 2,
    alignItems: 'center',
    justifyContent: 'center'
  },
  plusItem: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#929292'
  }
};

export default class ImagesPreview extends React.Component {
  render() {
    const { images } = this.props;
    if (images.length === 0) return <div />;
    const firstImage = images[0];
    const otherImagesToPreview = 3;
    const limit = images.length >= otherImagesToPreview ? otherImagesToPreview : images.length;
    const otherImages = images.length > 1 ? images.slice(1, limit) : [];
    const nbHiddenImages = limit === otherImagesToPreview ? images.length - otherImagesToPreview : 0;
    return (
      <div onPress={this.onPress} style={styles.imagesContainer}>
        <div style={styles.itemsContainer}>
          <div style={otherImages.length > 0 ? styles.firstItemContainer : styles.globalItemContainer}>
            <img alt="" src={`${firstImage.url}/big`} style={styles.firstItem} />
          </div>
          <div style={styles.otherItemsContainer}>
            {otherImages.map((image, key) => {
              return <img alt="" key={key} src={`${image.url}/small`} style={styles.otherItem} />;
            })}
            {nbHiddenImages
              ? <div style={styles.plusItemContainer}>
                <span style={styles.plusItem}>{`+${nbHiddenImages}`}</span>
              </div>
              : undefined}
          </div>
        </div>
      </div>
    );
  }
}