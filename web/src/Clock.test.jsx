import { render, screen } from '@testing-library/react';
import Clock from './Clock';

test('Renders clock showing time in the corret format', () => {
  //Given
  jest.useFakeTimers()
  jest.setSystemTime(new Date('1980-12-19T08:00:00'));
  render(<Clock />);

  //When
  const currenTimeElement = screen.getByTestId('current-time');

  //Then
  expect(currenTimeElement).toBeInTheDocument();
  const timeText = screen.getByTestId('current-time').textContent;
  expect(timeText).toMatch(/\d{2}:\d{2}:\d{2}/);
  expect(timeText).toBe('08:00:00');
});
