import React from 'react';
import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { createRender } from '@material-ui/core/test-utils';
import { MuiThemeProvider } from '@material-ui/core/styles';

import Alert from '../../../../js/app/components/common/Alert';
import theme from '../../../../js/app/theme';

configure({ adapter: new Adapter() });

describe('Alert component', () => {
  it('should render a danger alert', () => {
    const renderer = createRender();
    const component = renderer(
      <MuiThemeProvider theme={theme}>
        <Alert dismissible type="danger">
          Foo Bar
        </Alert>
      </MuiThemeProvider>
    );
    expect(component).toMatchSnapshot();
  });
});