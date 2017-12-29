import React from 'react';
import Icon from 'material-ui/Icon';

const styles = {
  icon: {
    marginRight: 5,
    color: '#666666ff'
  },
  keywordsContainer: {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingLeft: 15,
    paddingRight: 5,
    marginBottom: 5
  },
  keywordsText: {
    color: '#666666ff',
    marginLeft: 4,
    fontSize: 12
  }
};

const Keywords = ({ keywords }) => {
  const KeywordPressHandler = (k) => {
    console.log(k);
  };

  return (
    <div style={styles.keywordsContainer}>
      <Icon style={styles.icon} className={'mdi-set mdi-tag-multiple'} />
      {keywords.map((k, index) => {
        return (
          <div
            hitSlop={{ top: 15, bottom: 15, left: 15, right: 15 }}
            key={k}
            title={k}
            onClick={() => {
              return KeywordPressHandler(k);
            }}
          >
            <span style={styles.keywordsText}>
              {k}
              {index + 1 !== keywords.length ? ',' : ''}
            </span>
          </div>
        );
      })}
    </div>
  );
};

export default Keywords;