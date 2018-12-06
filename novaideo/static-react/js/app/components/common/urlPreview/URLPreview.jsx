// @flow
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Avatar from '@material-ui/core/Avatar';

import Embed from './Embed';
import ImagesPreview from '../ImagesPreview';
// For a future development (integration of graphs ...)
// import Frame from './Frame';

const styles = {
  container: {
    borderLeftColor: '#e8e8e8',
    borderLeftWidth: 3,
    paddingLeft: 10,
    marginBottom: 5,
    borderLeftStyle: 'solid',
    textAlign: 'initial'
  },
  integretedContainer: {
    backgroundColor: 'white',
    border: 'solid 1px #e8e8e8',
    borderRadius: 5,
    padding: '10px 25px',
    wordWrap: 'initial',
    fontStyle: 'normal',
    fontWeight: 400,
    whiteSpace: 'initial',
    letterSpacing: 'initial',
    margin: 15,
    display: 'grid'
  },
  header: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    padding: '5px 0',
    marginBottom: 5
  },
  headerAvatar: {
    width: 16,
    height: 16,
    maxWidth: 16,
    borderRadius: 3,
    borderWidth: 0.5,
    borderColor: '#d6d7da',
    marginBottom: 2
  },
  avatarRoot: {
    borderRadius: 4
  },
  avatar: {
    height: 30,
    width: 30
  },
  headerTitle: {
    display: 'flex',
    fontSize: 15,
    color: '#717274',
    justifyContent: 'space-around',
    paddingLeft: 5
  },
  contributionTitle: {
    color: '#337ab7',
    fontSize: 15,
    fontWeight: 'bold',
    paddingLeft: 5,
    textDecoration: 'none'
  },
  image: {
    width: 300,
    height: 150,
    borderRadius: 3,
    borderWidth: 0.5,
    borderColor: '#d6d7da',
    marginTop: 10,
    marginBottom: 10
  },
  url: {
    color: '#337ab7',
    fontWeight: 'bold',
    textDecoration: 'none'
  },
  description: {
    color: 'gray',
    paddingLeft: 5,
    fontSize: 12,
    lineHeight: '18px'
  },
  sliderHeader: {
    marginLeft: 4,
    fontSize: 17,
    color: 'white',
    width: '90%'
  },
  authorName: {
    color: 'gray',
    fontSize: 11,
    paddingLeft: 5
  },
  urlDataContainer: {
    display: 'flex',
    justifyContent: 'space-between',
    paddingBottom: 5,
    paddingTop: 10
  },
  urlDataEntryContainer: {
    display: 'flex',
    flexDirection: 'column'
  },
  urlDataLabel: {
    fontSize: 13,
    fontWeight: 'bold'
  },
  urlDataValue: {
    fontSize: 12
  },
  titleContainer: {
    display: 'flex',
    alignItems: 'center',
    width: '100%',
    justifyContent: 'space-between'
  }
};

type URLDataType = {
  label: string,
  data: string
};

export type URLPreviewProps = {
  // id: string,
  integreted?: boolean,
  url: string,
  html: string,
  title: string,
  description: string,
  thumbnailUrl: string,
  providerName: string,
  faviconUrl: string,
  authorName: string,
  authorAvatar: string,
  afterLoad: ?Function,
  data: Array<URLDataType>,
  classes: Object
};

class DumbURLPreview extends React.Component<URLPreviewProps, void> {
  static defaultProps = {
    integreted: false
  };

  componentDidMount() {
    const { html, afterLoad } = this.props;
    if (!html && afterLoad) afterLoad();
  }

  render() {
    // const { url, html, afterLoad } = this.props;
    // For a future development (integration of graphs ...)
    // If we have an integration HTML code, we need to include it into an iframe (the Frame component)
    // if (html) return <Frame id={url} html={html} afterLoad={afterLoad} />;
    const {
      integreted,
      authorName,
      authorAvatar,
      url,
      title,
      description,
      thumbnailUrl,
      providerName,
      faviconUrl,
      data,
      classes
    } = this.props;
    if (!description && !thumbnailUrl) return null;
    // isContribution like a twitter post
    const isContribution = authorName || authorAvatar;
    return (
      <div className={integreted ? classes.integretedContainer : classes.container}>
        {isContribution ? (
          <div className={classes.header}>
            <Avatar className={classes.avatar} classes={{ root: classes.avatarRoot }} size={10} src={authorAvatar} />
            <div className={classes.titleContainer}>
              <a target="_blank" href={url} className={classes.contributionTitle}>
                {title}
              </a>
              <div className={classes.authorName}>{authorName}</div>
            </div>
          </div>
        ) : (
          <div>
            <div className={classes.header}>
              {faviconUrl && <img alt="favicon" className={classes.headerAvatar} src={faviconUrl} />}
              <span className={classes.headerTitle}>{providerName}</span>
            </div>
            <div>
              <a target="_blank" href={url} className={classes.url}>
                {title}
              </a>
            </div>
          </div>
        )}
        <div className={classes.description}>{description}</div>
        <Embed
          url={url}
          defaultEmbed={
            thumbnailUrl && (
              <ImagesPreview
                images={[{ url: thumbnailUrl, variations: [] }]}
                context={{
                  title: title,
                  author: {
                    title: authorName || providerName,
                    picture: { url: authorAvatar || faviconUrl, strictUrl: true }
                  }
                }}
              />
            )
          }
        />
        {data.length > 0 && (
          <div className={classes.urlDataContainer}>
            {data.map((dataEntry) => {
              return (
                <div key={dataEntry.label} className={classes.urlDataEntityContainer}>
                  <div className={classes.urlDataLabel}>{dataEntry.label}</div>
                  <div className={classes.urlDataValue}>{dataEntry.data}</div>
                </div>
              );
            })}
          </div>
        )}
        {isContribution ? (
          <div className={classes.header}>
            {faviconUrl && <img alt="favicon" className={classes.headerAvatar} src={faviconUrl} />}
            <span className={classes.headerTitle}>{providerName}</span>
          </div>
        ) : (
          undefined
        )}
      </div>
    );
  }
}

export default withStyles(styles)(DumbURLPreview);