#include <app-window.h>

int main()
{
    auto ui = AppWindow::create();

    ui->on_request_increase_value([ui]{
        ui->set_counter(ui->get_counter() + 1);
    });

    ui->run();
    return 0;
}
