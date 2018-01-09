/* eslint-disable react/no-array-index-key */
import React from 'react';
import { connect } from 'react-redux';
import Avatar from 'material-ui/Avatar';

import ImagesPreview from '../common/ImagesPreview';
import IconWithText from '../common/IconWithText';
import Url from '../common/Url';

const styles = {
  container: {
    paddingLeft: 15,
    paddingRight: 40
  },
  header: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    padding: 5,
    paddingLeft: 10
  },
  headerTitle: {
    display: 'flex',
    fontSize: 15,
    color: '#2c2d30',
    fontWeight: '900',
    justifyContent: 'space-around',
    paddingLeft: 10
  },
  headerAddOn: {
    fontSize: 10,
    color: '#999999ff',
    paddingLeft: 5
  },
  body: {
    display: 'flex',
    flexDirection: 'row',
    marginTop: -5
  },
  bodyLeft: {
    display: 'flex',
    width: 60,
    justifyContent: 'center',
    alignItems: 'center'
  },
  bodyContent: {
    display: 'flex',
    justifyContent: 'space-between',
    flexDirection: 'column',
    width: '100%'
  },
  contentText: {
    color: '#2c2d30',
    fontSize: 15,
    lineHeight: 1.5,
    wordWrap: 'break-word'
  },
  urlsContainer: {
    paddingRight: 30,
    paddingLeft: 10,
    marginTop: 15,
    maxWidth: 400
  },
  bodyFooter: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'flex-end'
  },
  actionsText: {
    fontSize: 14,
    color: 'gray',
    marginLeft: 8,
    marginRight: 50
  },
  actionsIcon: {
    marginTop: 1
  }
};

export class DumbCommentItem extends React.Component {
  render() {
    const { node, itemdata } = this.props;
    const unreadComments = itemdata.channel
      ? itemdata.channel.unreadComments.map((comment) => {
        return comment.id;
      })
      : [];
    const isUnread = unreadComments.includes(node.id);
    const author = node.author;
    const authorPicture = author.picture;
    const createdAt = node.createdAt; // Moment(node.createdAt).format(I18n.t('datetimeFormat'));
    const images = node.attachedFiles
      ? node.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    return (
      <div style={styles.container}>
        <div style={styles.header}>
          <Avatar size={40} src={authorPicture ? `${authorPicture.url}/profil` : ''} />
          <span style={Object.assign({}, styles.headerTitle, isUnread ? { color: '#ef6e18' } : {})}>
            {author.title}
          </span>
          <span style={Object.assign({}, styles.headerAddOn, isUnread ? { color: '#ef6e18' } : {})}>
            {createdAt}
          </span>
        </div>
        <div style={styles.body}>
          <div style={styles.bodyLeft} />
          <div style={styles.bodyContent}>
            <div>
              <div style={styles.contentText}>
                {node.text}
              </div>
              <ImagesPreview images={images} />
            </div>
            <div style={styles.urlsContainer}>
              {node.urls.map((url, key) => {
                return <Url key={key} data={url} onPressUrlImage />;
              })}
            </div>
            {node.lenComments > 0
              ? <div style={styles.bodyFooter}>
                <IconWithText
                  styleText={styles.actionsText}
                  styleIcon={styles.actionsIcon}
                  name="comment-multiple-outline"
                  iconSize={15}
                  iconColor="gray"
                  text={`${node.lenComments} ${`reply${node.lenComments > 1 ? '*' : ''}`}`}
                />
              </div>
              : null}
          </div>
        </div>
      </div>
    );
  }
}

export const mapStateToProps = (state) => {
  return {};
};

export default connect(mapStateToProps)(DumbCommentItem);