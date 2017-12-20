import React from 'react';

const styles = {
  container: {
    borderLeftColor: '#e8e8e8',
    borderLeftWidth: 3,
    paddingLeft: 10,
    marginBottom: 5
  },
  header: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    padding: 5
  },
  headerAvatar: {
    width: 15,
    height: 15,
    borderRadius: 3,
    borderWidth: 0.5,
    borderColor: '#d6d7da'
  },
  authorAvatar: {
    width: 20,
    height: 20,
    borderRadius: 3,
    borderWidth: 0.5,
    borderColor: '#d6d7da'
  },
  headerTitle: {
    display: 'flex',
    fontSize: 13,
    color: '#999999ff',
    justifyContent: 'space-around',
    paddingLeft: 5
  },
  contributionTitle: {
    fontSize: 13,
    paddingLeft: 5,
    width: '99%'
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
    color: '#337ab7'
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

export default class Url extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
    this.state = {
      opened: false
    };
    this.onPress = this.onPress.bind(this);
    this.onClose = this.onClose.bind(this);
    this.getImageHeader = this.getImageHeader.bind(this);
  }

  render() {
    const { data } = this.props;
    return (
      <div style={styles.container}>
        {data.authorName || data.authorAvatar
          ? <div style={styles.header}>
            <img style={styles.authorAvatar} src={data.authorAvatar} />
            <div onPress={this.handleClick}>
              <span numberOfLines={1} style={styles.contributionTitle}>
                {data.title}
              </span>
              <span numberOfLines={1} style={styles.authorName}>
                {data.authorName}
              </span>
            </div>
          </div>
          : <div>
            <div style={styles.header}>
              <img style={styles.headerAvatar} src={data.favicon} />
              <span style={styles.headerTitle}>
                {data.siteName}
              </span>
            </div>
            <div onPress={this.handleClick}>
              <span style={styles.url}>
                {data.title}
              </span>
            </div>
          </div>}
        <span style={styles.description}>
          {data.description}
        </span>
        <div onPress={this.onPress}>
          <img src={data.imageUrl} style={styles.image} />
        </div>
        {data.authorName || data.authorAvatar
          ? <div style={styles.header}>
            <img style={styles.headerAvatar} src={data.favicon} />
            <span style={styles.headerTitle}>
              {data.siteName}
            </span>
          </div>
          : undefined}
      </div>
    );
  }
}