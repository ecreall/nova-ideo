import React from 'react';
import { withStyles } from 'material-ui/styles';
import Avatar from 'material-ui/Avatar';

import ImagesPreview from './ImagesPreview';

const styles = (theme) => {
  return {
    container: {
      borderLeftColor: '#e8e8e8',
      borderLeftWidth: 3,
      paddingLeft: 10,
      marginBottom: 5,
      borderLeftStyle: 'solid'
    },
    header: {
      display: 'flex',
      flexDirection: 'row',
      alignItems: 'center',
      padding: 5
    },
    headerAvatar: {
      width: 16,
      height: 16,
      borderRadius: 3,
      borderWidth: 0.5,
      borderColor: '#d6d7da'
    },
    avatarRoot: {
      borderRadius: 4
    },
    avatar: {
      color: theme.palette.tertiary.hover.color,
      backgroundColor: theme.palette.tertiary.color,
      fontWeight: 900
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
      width: '99%',
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
      fontSize: 12
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
    }
  };
};

class Url extends React.Component {
  render() {
    const { data, classes } = this.props;
    return (
      <div className={classes.container}>
        {data.authorName || data.authorAvatar
          ? <div className={classes.header}>
            <Avatar classes={{ root: classes.avatarRoot }} size={10} src={data.authorAvatar} />
            <div>
              <a target="_blank" href={data.url} className={classes.contributionTitle}>
                {data.title}
              </a>
              <span className={classes.authorName}>
                {data.authorName}
              </span>
            </div>
          </div>
          : <div>
            <div className={classes.header}>
              <img alt="favicon" className={classes.headerAvatar} src={data.favicon} />
              <span className={classes.headerTitle}>
                {data.siteName}
              </span>
            </div>
            <div>
              <a target="_blank" href={data.url} className={classes.url}>
                {data.title}
              </a>
            </div>
          </div>}
        <span className={classes.description}>
          {data.description}
        </span>
        {data.imageUrl && <ImagesPreview images={[{ url: data.imageUrl, variations: [] }]} />}
        {data.authorName || data.authorAvatar
          ? <div className={classes.header}>
            <img alt="favicon" className={classes.headerAvatar} src={data.favicon} />
            <span className={classes.headerTitle}>
              {data.siteName}
            </span>
          </div>
          : undefined}
      </div>
    );
  }
}

export default withStyles(styles)(Url);