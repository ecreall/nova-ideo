/* eslint-disable react/no-array-index-key */
import React from 'react';
import VisibilitySensor from 'react-visibility-sensor';
import Measure from 'react-measure';

export class ListItem extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      dimensions: {
        height: this.props.itemHeightEstimation
      }
    };
  }
  render() {
    const { height } = this.state.dimensions;
    return (
      <VisibilitySensor partialVisibility>
        {({ isVisible }) => {
          return (
            <Measure
              bounds
              onResize={(contentRect) => {
                this.setState({ dimensions: contentRect.bounds });
              }}
            >
              {({ measureRef }) => {
                return (
                  <div ref={measureRef} style={{ width: '100%', minHeight: isVisible ? 'auto' : height }}>
                    {isVisible ? this.props.children : null}
                  </div>
                );
              }}
            </Measure>
          );
        }}
      </VisibilitySensor>
    );
  }
}

export default ListItem;