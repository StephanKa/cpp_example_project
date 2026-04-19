#pragma once

#include <QObject>
#include <QTimer>
#include <QtQml/qqmlregistration.h>

class Backend : public QObject
{
    Q_OBJECT
    QML_ELEMENT

    Q_PROPERTY(int elapsedSeconds READ elapsedSeconds NOTIFY elapsedSecondsChanged)
    Q_PROPERTY(bool running READ running NOTIFY runningChanged)

public:
    explicit Backend(QObject *parent = nullptr) : QObject(parent)
    {
        connect(&m_timer, &QTimer::timeout, this, &Backend::onTick);
        m_timer.setInterval(1000);
    }

    [[nodiscard]] int  elapsedSeconds() const { return m_elapsedSeconds; }
    [[nodiscard]] bool running()        const { return m_timer.isActive(); }

public slots:
    void start()
    {
        m_elapsedSeconds = 0;
        emit elapsedSecondsChanged();
        m_timer.start();
        emit runningChanged();
    }

    void stop()
    {
        m_timer.stop();
        emit runningChanged();
    }

    void reset()
    {
        m_timer.stop();
        m_elapsedSeconds = 0;
        emit elapsedSecondsChanged();
        emit runningChanged();
    }

signals:
    void elapsedSecondsChanged();
    void runningChanged();

private slots:
    void onTick()
    {
        ++m_elapsedSeconds;
        emit elapsedSecondsChanged();
    }

private:
    QTimer m_timer;
    int    m_elapsedSeconds{0};
};
