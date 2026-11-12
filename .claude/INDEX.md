# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11342  GET              /                                                dashboard
 13399  GET              /api/abo/status                                  api_abo_status
 13353  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 12130  GET              /api/automation/status                           api_automation_status
 12152  POST             /api/automation/toggle                           api_automation_toggle
 22032  GET              /api/channel/categories                          api_channel_categories
 22038  POST             /api/channel/set                                 api_channel_set
 21885  GET              /api/channels/status                             api_channels_status
 21559  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21542  GET              /api/clips                                       api_clips
 21588  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21460  GET              /api/debug/threads                               api_debug_threads
 13364  GET              /api/events                                      api_events
 12843  GET              /api/events/stream                               api_events_stream
 12670  GET              /api/health                                      api_health
 21501  POST             /api/highlights/config                           api_highlights_config
 11272  POST             /api/login                                       dashboard_login_submit
 13689  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12758  GET              /api/notify/status                               api_notify_status
 12769  POST             /api/notify/test                                 api_notify_test
 13453  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13430  GET              /api/proxy/trend                                 api_proxy_trend
 21608  GET              /api/tts/<fn>                                    api_tts_file
 22396  GET              /api/upload_window                               api_upload_window
 12960  GET              /archive/<int:eid>/download                      archive_download
 12988  GET              /download/<int:recording_id>                     download
 12917  GET              /health                                          health
 21332  GET              /healthz                                         healthz
 11263  GET              /login                                           dashboard_login_page
 11297  GET              /logout                                          dashboard_logout
 11304  GET              /manifest.webmanifest                            pwa_manifest
 22369  GET              /overlay                                         overlay_page
 11328  GET              /pwa-icon-<variant>.png                          pwa_icon
 11314  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (345)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1023  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   764  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   894  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   874  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   912  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   832  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   382  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   393  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   403  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   426  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   433  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   444  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   572  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   670  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1261  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1293  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   367  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   976  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   956  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1129  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1177  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1228  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1087  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   931  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   417  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   408  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   374  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   359  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   179  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   130  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    71  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    78  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   200  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   227  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   320  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   264  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   282  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   187  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   125  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   139  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   154  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   222  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   242  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   269  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   225  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   247  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   174  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   131  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   181  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   229  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   212  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   121  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   539  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   591  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   613  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   552  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   578  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   415  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   405  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   440  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   237  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   458  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   487  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   407  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   516  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   393  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   268  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   337  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   324  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   164  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   282  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   133  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   374  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   429  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2285  /about                  Ueber diesen Bot
   981  /ai                     
  2285  /aireset                KI-Kontext zuruecksetzen
  1399  /ask                    
  1082  /assign_role            
  1132  /ban                    
  2240  /botstats               
  2285  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2285  /bulkadd                Mehrere User auf einmal tracken · a b c
  2285  /cleanup                Alte Aufnahmen aufraeumen
  1665  /clearwarns             
  2204  /clip                   
  2189  /clipoftheweek          
  1535  /clips                  
  2285  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1037  /create_category        
  1008  /create_channel         
  1072  /create_group           
  1047  /create_role            
  1023  /create_voice           
  1276  /daily                  
  2285  /diag                   Vollstaendige Diagnose
  2285  /einnahmen              Einnahmen und Spenden
  1428  /event                  
  1470  /events                 
  1575  /follow                 
  1564  /help                   
  1122  /kick                   
  1248  /leaderboard            
  2285  /live                   Live-Status sofort pruefen · @user
  1522  /livenow                
  2285  /logs                   Letzte Fehler aus dem Log
  2285  /pause                  Tracking pausieren · @user
  1550  /post_test              
  1360  /profile                
  1154  /purge                  
  2285  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2285  /quota                  Speicher-Quota
  1235  /rank                   
  1510  /recstatus              
  1092  /remove_role            
  2285  /report                 Azrael-Sentinel-Wochenreport
   994  /restream_status        
  2285  /resume                 Tracking fortsetzen · @user
  1102  /set_channel_perms      
  1197  /setup_community        
  1214  /setup_targets          
  1496  /spenden                
  1607  /stats                  
   953  /status                 
  2285  /stoprec                Laufende Aufnahme sauber beenden · @user
  1703  /streaminfo             
  2285  /summary                Tageszusammenfassung
  2285  /sysres                 System-Ressourcen
  2285  /teststream             Recorder-Selbsttest · @user
  2285  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1142  /timeout                
  1675  /topstreamers           
  2285  /topusers               Top-Streamer nach Aufnahmen
   883  /track                  
  2285  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   966  /tracklist              
  1589  /unfollow               
  2285  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   915  /untrack                
  1628  /warn                   
  1651  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2452  on_member_join
  2409  on_message
  2306  on_raw_reaction_add
  2487  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (54 Funktionen)

```
  1780-1831   _award_xp
   537-564    _bereich_umziehen
   484-494    _clip_kopieren
  2002-2031   _clip_week_leader
  2055-2069   _clipoftheweek_loop
  2604-2666   _community_events_loop
  1737-1759   _dc_client
  1762-1771   _dc_offen
  2706-2741   _disc_automod_check
   410-415    _disc_sprache_setzen
  1834-1882   _discord_ai_automod
   686-725    _discord_automod
  1885-1905   _discord_azrael_reply
  2072-2563   _discord_run_once
   245-303    _discord_start
   306-360    _ensure_discord_invite
  2569-2601   _ensure_error_channel
   431-444    _ensure_rank_roles
   846-860    _ensure_team_roles
  2669-2699   _error_channel_loop
   735-739    _guard
   655-683    _handle_voice_ai
   418-428    _is_admin
   509-534    _link_video
  1950-1961   _liveboard_loop
   742-775    _on_level_up
   651-652    _par_chat_id
  2034-2052   _post_clip_of_week
  1964-1982   _post_weekly_digest
   447-473    _provision_base_channels
  1502-1596   _reg_betrieb
  1168-1265   _reg_community_setup
  1268-1349   _reg_daily_profil
  1392-1489   _reg_frage_events
   940-996    _reg_info
  1114-1165   _reg_moderation
  1352-1389   _reg_profil
  1063-1111   _reg_rollen
   999-1060   _reg_server
  1492-1499   _reg_spenden
  1599-1686   _reg_streamer
  1689-1734   _reg_system
   874-937    _reg_tracking
   810-843    _run_tg_handler
   638-648    _tracked_usernames
   162-224    _uebernehmen
   497-506    _umzugsmarken
  1914-1947   _update_liveboard
  1985-1999   _weekly_digest_loop
   476-481    _ziel_guild
   567-609    _ziele_abgleichen
   618-635    _ziele_sync_loop
   612-615    _ziele_takt_min
   227-230    starte
```

## Top-Level-Symbole in bot.py (616 Funktionen, 4 Klassen)

```
 27589-27611  _abbruch_datenbank_unlesbar
  2845-2846   _abo_key
  2866-2884   _abo_probe_dump
 27711-27727  _abschied_wachen
 27730-27748  _abschluss
 17562-17569  _ad_allowlist
 18728-18734  _agent_for
 18737-18753  _ai_telemetry
 19273-19291  _alert
 23264-23314  _alert_monitor_loop
 19978-20035  _alte_beilagen_einsammeln
 23696-23758  _announce_loop
  3797-3807   _anthropic_key
  3814-3816   _anthropic_model
 10831-10834  _arg_int
  2837-2842   _as_dict
 27275-27284  _async_exc_handler
 19462-19484  _audio_tap_cmd
 20498-20557  _audio_tap_melden
 19498-19522  _audio_tap_sammler
 10177-10214  _aufnahme_beim_stopp_sichern
 19920-19941  _aufnahme_chat_ausklang
 19904-19917  _aufnahme_chat_beginnen
 20063-20084  _aufnahme_chat_dienst
 20257-20310  _aufnahme_chat_einarbeiten
 19899-19901  _aufnahme_chat_modus
 20087-20136  _aufnahme_chat_nachtrag
 19944-19975  _aufnahme_chat_vormerken
 20054-20060  _aufnahme_chat_wecken
 26399-26401  _aufnahme_deckel
 20139-20160  _aufnahme_fertigmachen
 23933-23986  _aufnahme_nach_discord
 10217-10235  _aufnahme_platz_frei
 10120-10147  _aufnahme_verteilen
 27675-27695  _aufnahmen_abschliessen
 27614-27672  _aufraeumen
 11105-11174  _auth_cookie
 11061-11101  _auth_guard
  2072-2077   _auto_on
 21184-21202  _auto_restream_loop
 15034-15076  _avatar_frames_laden
 17612-17625  _azrael_brain_kontext
 24892-24907  _azrael_broadcast_reply
 24792-24814  _azrael_chat_reply
 24764-24789  _azrael_chat_should_reply
 24820-24822  _azrael_gate_cfg
  4262-4275   _azrael_ki
 18758-18772  _azrael_live_state
  4278-4300   _azrael_lokal
 22282-22296  _azrael_overlay_state
 18814-18822  _azrael_persona_kern
 19155-19209  _azrael_proactive_loop
 18576-18632  _azrael_reaction_to_chats
 24825-24832  _azrael_reply_all_chats
  4303-4318   _azrael_schweigt_melden
 24751-24761  _azrael_self_names
 24860-24889  _azrael_send_to
 14995-15031  _azrael_spricht
 15342-15355  _azrael_stimme_stumm
 18778-18811  _azrael_system
 23398-23401  _backup_active
 23479-23492  _backup_loop
  5641-5664   _betreiber_pruefen
 26488-26492  _betrieb
 27348-27357  _brain_crowdsec_snap
 27516-27519  _brain_db_health
 23185-23194  _brain_growth_loop
 11521-11548  _brain_growth_snapshot
  2756-2790   _brain_hint_delay
 27420-27455  _brain_moderation_snap
  6915-6943   _brain_notify
 27522-27544  _brain_recording_snap
 27360-27417  _brain_restream_health
 27547-27560  _brain_tiktok_status_snap
 12822-12839  _browser_push
  6955-7042   _build_daily_summary
 15389-15393  _build_restream_cmd
  5667-5694   _can_stop_tracking
  2185-2207   _capture_set_cookies
 13507-13510  _cfg_get
 13513-13515  _cfg_set
 21993-22028  _channel_set_all
 14086-14089  _chat_connected
 14092-14108  _chat_disconnected
 20048-20051  _chat_einarbeiten_async
  9611-9641   _chat_is_forum
 19868-19893  _chat_listener_abbauen
  9783-9818   _chat_migriert
  9821-9822   _chat_migriert_async
 14128-14130  _chat_sanitize
 14071-14083  _chat_stat
 14111-14114  _chat_stats_snapshot
  4132-4144   _check_ai_models_sync
 11803-11846  _classify_pool_anonymity
 11849-11866  _classify_pool_anonymity_bg
   920-942    _claude_chat_sync_metered
 10863-10869  _client_ip
 24391-24405  _clip_chat_ass
 23842-23876  _clip_prune
 23879-23889  _clip_recfile_for
 24311-24379  _clip_schneiden
 24408-24414  _clip_should_velocity
 23989-24074  _clip_to_discord
 20228-20233  _clips_abwarten
  4001-4010   _close_ai_session
 24938-24953  _cohost_broadcast
 24923-24924  _cohost_cfg
 24979-24991  _cohost_fire_highlight
 24927-24935  _cohost_gate
 24956-24976  _cohost_highlight
 11451-11453  _conv_messages
  7339-7400   _cookie_alarm_loop
  2275-2276   _cookie_autofetch_info
  2259-2263   _cookie_autorefresh_info
 26949-26971  _cookie_bezug_loop
 26974-26999  _cookie_bezug_runde
  2162-2166   _cookie_header
 10872-10877  _cookie_sicher
  2288-2302   _cookies_selbst_holen
  4427-4429   _create_index_safe
 22728-22842  _crowdsec_status
 22674-22725  _crowdsec_via_lapi
 22578-22596  _cscli_bin
 22605-22618  _cscli_path
  7223-7250   _daily_summary_loop
 22636-22653  _darf_journal_lesen
  3322-3347   _darf_ytdlp_nachschlagen
 13003-13024  _dashboard_adresse
 10892-10896  _dashboard_hostnamen
  1524-1554   _dashboard_trackings_umziehen
 24382-24388  _datei_weg
 23238-23261  _db_maintenance_loop
  7173-7220   _db_vacuum_loop
 17585-17609  _detect_foreign_ad
  1752-1763   _diag_path_owner
 19060-19105  _director_finalize
 20487-20494  _director_for
 19009-19057  _director_mark
 24224-24227  _disc_state_get
 24230-24237  _disc_state_set
 23166-23175  _discord_bot_starten
 23129-23140  _discord_einladung_merken
 23178-23182  _discord_invite
 23143-23163  _discord_kontext
 24185-24221  _discord_live_thread
 19212-19224  _discord_notify
 23101-23126  _discord_ops_alert
 24085-24181  _discord_post_user
 23761-23767  _discord_stop
  7253-7334   _disk_alarm_loop
 26820-26871  _disk_autoclean
 27130-27143  _disk_guard_loop
 14973-14980  _drossel_hoeher
 14969-14970  _drossel_stufe
 14983-14991  _drossel_zuruecksetzen
 13180-13182  _dump_all_threads
 26495-26509  _einstellungen_startzeile
 11729-11792  _enrich_proxies_with_geo
  2331-2392   _ensure_cookie_file_netscape
  9712-9715   _ensure_notify_topic
 11973-12010  _ensure_proxy_ready
  9651-9674   _ensure_topic
   761-763    _env_int
   766-768    _env_int_range
 19257-19270  _event_webhook
 13854-13867  _evolution_loop
  6356-6390   _extract_file_payload
  2464-2466   _extract_urls_from_streamurl_node
 22621-22628  _f2b_sudo_hint
  1510-1521   _fanout_ziele
 27751-27814  _fatal_vom_botteil
 26404-26419  _fd_grenze_anheben
  5101-5111   _fehler_text
 11630-11648  _fetch_proxy_list
 19837-19865  _fetch_tiktok_room_id
   846-849    _ff_cmd
 20241-20254  _ffprobe_masse
 14917-14933  _fifo_schreiber_wecken
 14727-14732  _find_chromium
  3717-3719   _find_external_recorder
  2469-2471   _find_stream_urls
 13558-13583  _fire_webhooks
  8272-8282   _fork_safe
   953-966    _freeai_chat_sync_metered
 22667-22671  _geo_lookup_ips
  3989-3998   _get_ai_session
  8100-8140   _get_live_info
  3166-3173   _get_resolve_semaphore
  8799-9220   _handle_single_tracking
 26604-26606  _hb
 26609-26626  _hb_while
 21445-21456  _healthz_fuer_aufrufer
 26650-26678  _heap_zurueckgeben
 11178-11195  _herkunft_guard
 14142-14144  _highlight_cfg
 14147-14176  _highlight_observe
 14778-14786  _htmlov_bild_schreiben
 14756-14775  _htmlov_dauerbrowser
 14735-14753  _htmlov_screenshot_cmd
 19524-19534  _httpx_proxy
 13591-13603  _in_quiet_hours
 27575-27586  _init_db_oder_abbruch
 28401-28432  _install_fast_eventloop
 10726-10780  _install_fast_json
 13185-13201  _install_faulthandler
 21235-21244  _intel_ensure_schema
 21287-21322  _intel_index_loop
 21256-21271  _intel_index_one
 21247-21253  _intel_semantic
  5626-5639   _is_authorized
  8625-8646   _is_dead
  2454-2456   _is_hevc
 22656-22658  _is_private_ip
  1971-1978   _is_process_running
  6945-6952   _is_quiet_hours
  1412-1421   _is_upload_window
  4966-4981   _iso
 10880-10889  _ist_lokal
 10815-10828  _json_error_handler
  4058-4067   _ki_rueckfall_melden
  7167-7168   _kick_broadcaster_id
  8500-8507   _kick_cluster_gefunden
  8435-8497   _kick_cluster_weiter
  7079-7121   _kick_follower_count
  7063-7066   _kick_slug
 12635-12642  _kick_user_token
  8405-8432   _kick_ws_pause
 27563-27572  _kickmod_boot
  4511-4514   _kind_from_filename
 26915-26918  _lagebild_discord_aufnahme
 26928-26932  _lagebild_kick_chat
 26921-26925  _lagebild_overlay
 26935-26937  _lagebild_spendenziel
 26902-26912  _lagebild_upload
 13620-13622  _latest_popularity
  1908-1917   _laufstand
 27090-27127  _laufstand_loop
 26528-26566  _leistung_erheben
  7974-8001   _link_video_senden
  8786-8797   _live_check_frist_melden
  2900-2913   _live_ohne_stream
 20893-20942  _live_react_loop
 20560-20882  _live_react_worker
  3565-3679   _live_status_aufloesen
 18635-18646  _live_transcript_push
 20884-20891  _live_users
 19108-19152  _living_title_loop
 23404-23476  _local_backup_scan
  4906-4929   _lock_update
 10797-10811  _log_5xx
 26569-26601  _log_schleuse_pruefen
   836-843    _log_sicher
 15401-15413  _looks_like_codec_err
 15396-15398  _looks_like_source_expired
  8323-8353   _loop_fehler
 13205-13214  _loop_heartbeat
 26310-26343  _loop_lag_monitor
 26357-26377  _loop_stockung_melden
 26380-26390  _loop_takt_starten
 13217-13290  _loop_watchdog_thread
 18512-18529  _loyalty_add
 18503-18509  _loyalty_get
 18532-18540  _loyalty_top
  5308-5327   _manual_status
  8648-8649   _mark_dead
 12249-12265  _marketing_loop
 24839-24857  _maybe_handle_command
 27229-27253  _maybe_hype_clip
 23811-23839  _meme_klassifizieren
 20163-20225  _meme_zusammenschnitt
  4414-4419   _migrate_columns
 25121-25132  _mod_is_exempt
 25135-25140  _mod_warn_first
 25143-25146  _mod_warn_text
 13911-13930  _modlog
 13894-13908  _modlog_schreiben
  1108-1110   _multistream_targets
  3350-3386   _nachschlag_ytdlp
  8285-8286   _nc_create_subprocess_exec
  8289-8290   _nc_create_subprocess_shell
 12572-12589  _news_loop
 13953-13955  _normalize_ingest
  2687-2704   _note_check_duration
  9706-9709   _notify_topic_name
  2891-2897   _offline_ergebnis
  3389-3412   _ohne_url_melden
 18661-18669  _oracle_memories
 18958-18992  _oracle_memorize
 18672-18685  _oracle_persona
 18654-18658  _oracle_recent_text
 14351-14352  _ov_atomic_write
 14342-14344  _ov_bar
 17488-17500  _ov_clip_text
 14347-14348  _ov_oneline
 22333-22362  _overlay_push
 14681-14724  _overlay_render_size
 14022-14026  _overlay_session_reset
 22298-22300  _overlay_src_ok
 14361-14373  _overlay_takt
 17572-17582  _own_invites
 14676-14678  _parse_size
 22850-22930  _parse_ssh_attacks
  7650-7683   _pause_resume_cmd
  2213-2257   _persist_refreshed_cookies
  2116-2148   _pick_checked_pull_proxy
 10946-10961  _pin_auth_value
 11050-11051  _pin_clear_fail
 11014-11017  _pin_global_gesperrt
 10967-10978  _pin_hmac_schluessel
 11020-11027  _pin_locked
 11030-11047  _pin_note_fail
 10981-11002  _pin_ok
 22126-22151  _piper_pick_model
 22211-22276  _piper_say
 13520-13555  _post_json_threaded
 14655-14673  _probe_video_size
  1999-2016   _proc_is_recorder
 11942-11970  _proxy_pool_refresh_loop
  2082-2113   _proxy_report_recording
  9359-9440   _pruef_runde
  9318-9356   _pruefstand_melden
 26439-26450  _pruefung_verworfen
 13170-13172  _prune_stall_dumps
 12319-12491  _public_stats
  2279-2285   _pull_proxy_still
 19228-19254  _push_notify
 11242-11244  _pwa_dir
 11699-11714  _quick_validate_proxy
 13586-13588  _quiet_hours_config
 11207-11240  _rate_guard
  2916-2944   _raumsperre_fragen
 18473-18479  _react_warn
  8187-8226   _reap_proc
 10899-10915  _rebinding_melden
 10050-10117  _rec_auto_abschalten
  9997-10047  _rec_frueh_getrennt
  9862-9942   _rec_kategorie_melden
  9945-9994   _rec_totstreak_fortschreiben
  2727-2749   _record_check_outcome
   831-833    _redact_stream_urls
 11869-11939  _refresh_proxy_pool
  2504-2595   _resolve_via_html
  2947-3143   _resolve_via_webcast_api_v2
  3211-3298   _resolve_via_ytdlp
 24448-24577  _resolve_youtube_ingest
  2480-2501   _resolver_stumm
 14005-14016  _restream_active_sources
 15079-15206  _restream_avatar_feeder_start
 15209-15219  _restream_avatar_feeder_stop
 20313-20451  _restream_chat_guardian
 14179-14251  _restream_chat_push
 14328-14337  _restream_chat_push_async
 27458-27513  _restream_durchreicher
 14789-14914  _restream_html_overlay_start
 14936-14956  _restream_html_overlay_stop
 13964-13987  _restream_overlay_files
 20946-20978  _restream_platform_state
 21146-21181  _restream_resume_after_restart
 14282-14299  _restream_soll_schreiben
 14302-14325  _restream_status_schreiben
 15267-15339  _restream_tts_enqueue_wav
 14617-14649  _restream_tts_feeder
 14614-14615  _restream_tts_fifo_path
 15222-15249  _restream_tts_start
 15251-15265  _restream_tts_stop
 20984-21143  _restream_verify_loop
 23369-23381  _retention_loop
 23363-23366  _retention_scan
  2848-2850   _room_is_abo
  6394-6511   _run_ai_call
 13313-13326  _run_async_from_flask
 22661-22664  _run_priv
 28389-28397  _run_selfcheck_and_exit
 23384-23395  _s3_client
  8675-8745   _safe_send
  5234-5250   _sample_net_throughput
  2793-2823   _schedule_next_check
 23317-23360  _scheduler_loop
  4422-4424   _schema_pk
 13330-13335  _scraper_session
 25149-25188  _screen_full
 12686-12723  _sec_headers
  2459-2461   _select_stream_from_data_section
 28106-28386  _selfcheck
  9718-9752   _send_live_notice
  1435-1439   _should_defer_upload
 23892-23930  _shrink_for_discord
 11247-11259  _sicheres_ziel
 23197-23235  _sicherheits_erinnerung_loop
 27150-27167  _sign_health_check
 27170-27189  _sign_health_loop
  4984-5009   _sitzung_bestimmen
 21428-21438  _sparen_lage
  8302-8313   _spawn
 28820-28850  _spawn_from_flask
 26453-26459  _speicher_maps
 26462-26477  _speicher_pflegen
 19536-19834  _start_chat_listener
 26422-26436  _start_gesperrt
 13293-13310  _start_loop_watchdog
 12518-12567  _stats_loop
 12497-12500  _stats_output_path
 12503-12515  _stats_write
 22163-22177  _stimme_saubern
 22184-22208  _stimme_schon_gesagt
  9299-9315   _storage_cleanup_loop
 27209-27216  _story_for
  3742-3748   _stream_url_expiry
  3750-3755   _stream_url_ttl
 17535-17542  _streamer_persona_get
 23501-23653  _system_backup
 23662-23692  _system_backup_loop
 13130-13148  _task_auf_bot_schleife
 25986-26002  _telegram_befehlsmenue
  8356-8402   _telegram_polling_fehler
  1480-1507   _telegram_ziele
 11651-11690  _test_proxy
 12197-12213  _testpush_resolve_live
 20236-20238  _text_schreiben
  9770-9780   _tg_migriert_laden
  9766-9767   _tg_migriert_pfad
  8651-8672   _tg_sprache_setzen
  9580-9590   _tg_topics_load_into_mem
  9577-9578   _tg_topics_path
  9592-9599   _tg_topics_save
 10918-10928  _token_ok
  9677-9693   _topic_anlegen
  9602-9609   _topic_forget
 13606-13617  _tracking_max_duration
  4719-4733   _tracking_remove_cleanup
  4750-4762   _tracking_resume_cleanup
  1810-1833   _try_attach_file_handler
 22153-22161  _tts_cleanup
 12173-12177  _tunnel_effective
 26874-26894  _tunnel_lage
 27035-27087  _tunnel_wacht_loop
 21652-21705  _twitch_channel_status
 25191-25339  _twitch_chat_loop
 24243-24256  _twitch_clip_versuchen
 25002-25108  _twitch_eventsub_loop
  1600-1635   _upload_queue_abarbeiten
  1458-1478   _upload_queue_add
  1571-1573   _upload_queue_count
  1441-1450   _upload_queue_load
  1638-1660   _upload_queue_nachher
  1431-1433   _upload_queue_path
  1557-1561   _upload_queue_remove
  1452-1456   _upload_queue_save
  1564-1569   _upload_queue_update
 10150-10174  _upload_rest_sichern
  1575-1597   _upload_window_loop
  8160-8167   _uptime_s
 13941-13950  _url_host
  3415-3513   _url_nachschlag
   913-917    _usage_record_claude
 27323-27345  _v37_pause_source
 27287-27297  _v37_restream_restart
 27300-27320  _v37_unpause_source
  8574-8618   _verbindung_verloren
  7124-7155   _viewer_sample_loop
 11054-11057  _wants_html
  8170-8184   _warn_empty_env
 26681-26806  _watchdog_loop
 24723-24731  _wchat_thank_ok
 27002-27032  _werkzeug_wacht_loop
 19296-19334  _whisper_get_model
  8261-8269   _whisper_native_section
 18460-18466  _whisper_pool
 19428-19460  _whisper_segments
 19336-19352  _whisper_stumm
 19355-19425  _whisper_transcribe
 14414-14571  _write_restream_overlay
 14376-14411  _write_restream_overlay_async
 25363-25462  _youtube_api_chat_loop
 21708-21811  _youtube_api_status
 21814-21881  _youtube_channel_status
 25465-25629  _youtube_chat_loop
 24259-24284  _youtube_clip_versuchen
 24583-24596  _youtube_restream_autoconfig
 24599-24623  _youtube_restream_autoconfig_inner
 24690-24718  _youtube_send
 21949-21990  _youtube_set_channel
 24626-24660  _yt_access_token
 24663-24678  _yt_live_chat_id
 24686-24687  _yt_sendrate_cfg
 25342-25357  _yt_timeout
  3190-3191   _ytdlp_detect_available
  3206-3208   _ytdlp_einzeln
  3193-3204   _ytdlp_note_result
 13175-13177  _zombie_child_count
 26512-26525  _zustand_kennzahlen
  8036-8060   about
  4630-4634   add_ai_log_entry
  4547-4550   add_archive_entry
  5272-5274   add_archive_rule
  5012-5083   add_recording
  4694-4711   add_tracking
  6514-6547   ai
  4158-4253   ai_chat
  4352-4362   ai_history_append
  4364-4369   ai_history_clear
  4341-4350   ai_history_load
  4326-4339   ai_rate_limit_check
  6576-6584   aireset
 18825-18844  azrael_chat
 25634-25756  brain_cmd
  3758-3763   build_recording_cmd
  4714-4717   bulk_add_trackings
  7403-7462   bulkadd
  9443-9559   check_all_trackings
  4766-4778   claim_live_transition
 17628-18392  class KickModerator
 15416-17375  class RestreamManager
  4932-4933   class _AufnahmeLockVerloren
  8510-8571   class _KickClusterSuche
 12056-12098  classify_proxy_anonymity
  6622-6821   cleanup
  5562-5568   cleanup_old_recordings
  4957-4964   clear_recording
 24287-24308  clip_moment
  5224-5227   compute_storage_forecast
  7525-7601   cookies_cmd
  7604-7647   cookies_datei_cmd
  4685-4691   count_trackings_for_chat
  4617-4628   decide_preferred_recorder
  4557-4560   delete_archive_entry
  5276-5278   delete_archive_rule
  6051-6198   diag
 25868-25929  einnahmen_cmd
  5218-5221   find_recordings_by_fingerprint
  4578-4594   finish_recording_attempt
  4738-4740   get_all_active_trackings
  4645-4647   get_all_checks
  5085-5088   get_all_recordings
  5167-5169   get_all_tags_with_counts
  5195-5198   get_annotations_for_recording
  4552-4555   get_archive_entry
  5188-5191   get_bookmarked_recordings
  2319-2324   get_cookie_health
  5155-5161   get_event_log
  4601-4615   get_last_recording_attempt
  3516-3558   get_live_status
  5501-5504   get_manual_recordings
  5203-5206   get_or_compute_inspect_sync
  5603-5606   get_outcome_breakdown
  5174-5177   get_priority_poll_interval
  4596-4599   get_recent_recording_attempts
  5090-5093   get_recording_by_id
  5181-5184   get_recording_note
  3929-3958   get_redis
  4674-4677   get_stats
  5556-5560   get_storage_stats
  5296-5298   get_tiktok_status_distribution
  4780-4789   get_tracking_state
  4735-4736   get_trackings_for_group
  5517-5520   get_trash_recordings
 10238-10705  handle_recording_finished
 25978-25983  hilfe_cmd
  4437-4502   init_db
  5268-5270   list_archive_rules
  5836-5874   live
  8748-8778   live_check_worker
  4013-4055   llm_chat
  4090-4122   llm_chat_sync
  4075-4087   llm_list_models
  5114-5147   log_event
  1933-1966   log_recording_failure
  7797-7846   logs_cmd
 27817-28096  main
  6550-6573   on_ai_media
  7923-7949   on_ai_reply
  8004-8033   on_azrael_mention
  8065-8095   on_callback
  9825-9843   on_chat_migration
  7958-7971   on_link_video
 18850-18955  oracle_handle
  7686-7689   pause_tracking
  5616-5621   profile_keyboard
  5789-5833   quelle
  7748-7794   quota
  9222-9296   reaper_loop
  5292-5294   record_tiktok_status
  6589-6619   recstatus
  3960-3968   redis_get_json
  3971-3977   redis_set_json
 26005-26015  report_cmd
 12101-12103  report_proxy_result
  2598-2640   resolve_tiktok_live_stream
  5512-5515   restore_recording
  7692-7695   resume_tracking
  5281-5286   run_archive_rules
 26018-26290  run_bot
 13027-13121  run_flask
  5256-5259   sample_bandwidth_for_active
  4637-4643   save_tiktok_check
  4936-4955   set_recording_file
  4743-4747   set_tracking_paused
  5507-5510   soft_delete_recording
 25963-25975  spenden_cmd
  9849-9860   split_and_send_video
  5699-5741   start
  4562-4576   start_recording_attempt
  6824-6862   stats
  5446-5499   stop_manual_recording
  7698-7745   stoprec
  7048-7056   summary_cmd
  7849-7920   sysres
  6200-6344   teststream
  5743-5784   tiktok
  7465-7522   topusers
  5911-5968   track
  5876-5908   track_exact
  5982-6049   tracklist
  5330-5444   trigger_manual_recording
  4868-4903   try_acquire_recording_lock
  5523-5525   universal_search
 25932-25960  unpause_cmd
  5970-5980   untrack
 25759-25865  update_cmd
  5213-5216   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelkontext.py       ausfall, block, fakten, letzte_erinnerung, nachricht, restream_quellen, sicher, streamer_waehlen
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, host_ist_lokal, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, class KeinDesktop, configure, desktop_pruefen, hole_gastcookies, schreibe, uebernehmen, zusammenfuehren
cookies.py             configure, gesundheit, hat_login, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, mariadb_lage, set_pool, treiber_fehler, treiber_wunsch, vorrat_groesse, vorrat_lage, vorrat_leeren
dcspar.py              anzeige, client_optionen, puffer
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordaufnahme.py     an, beschriftung, hochladen, teilen
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, loeschbar, umzugsmarke, umzugsmarke_lesen
donations.py           configure, fmt_eur, kurse_aus_env, parse_number, source_allowed, summe_eur, to_eur, unknown_count, zeile_eur
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       bekannt, class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
encodeschlange.py      lage, last_frei, parallel, platz, platz_sync
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
forkriegel.py          class Vortritt
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
heapzaum.py            arenen_wunsch, deckeln, lage, rss_mb, takt_min, zurueckgeben
herkunft.py            entscheiden
highlights.py          check, new_state, observe, score, zustand
httpsitzung.py         schliessen, sitzung, teilen
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, state_gueltig, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              azrael_lage, azrael_wahl, backend, gesamtzeit, llm_zeiten, lokal_installiert, lokal_stand, lokal_zuerst, lokales_modell, normal, provider, vorrang, wartezeit, weg_zaehlen, zeitlimit
lagebild.py            bauen, dienst_quelle, dienste, dienste_lesen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
linkvideo.py           abklingzeit_s, an, aufraeumen, ausgabe_lesen, befehl, bildunterschrift, configure, darf, grund, holen, ist_tiktok, links, max_dauer_s, sperre, werkzeug
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
livemeldung.py         live_an, live_aus
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler, lage, teilen
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
piperarbeiter.py       main
piperdienst.py         an, beenden, lage, sprechen
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, runde_gelaufen, uebersicht, vergessen
pruefschlange.py       erledigt, mit_frist, vorgemerkt, vormerken, zuruecksetzen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
raumkennung.py         grund, gueltig
raumsperre.py          deuten, faellig, lage, merken, snapshot, text, vergessen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        ausnahme_text, class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
sitzungsschluessel.py  laden, pin_schluessel
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
spendeninfo.py         krypto, paypal, paypal_url, stand, text
spendenziel.py         eingang, fenster_start, ist_monatlich, stand, summe, zeitraum, ziel_eur
sqldialekt.py          bei_konflikt
sqlguard.py            abbruch_nach, check_readonly, frist_ueberschritten, frist_unbekannt, mariadb_mit_frist, normalize, with_limit
sqlutil.py             zeitfenster_literal
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             class BestandUnbekannt, cleanup, forecast, notfall_raeumen, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, text, zuruecksetzen
textmore.py            configure_banned_cap, pre_nachrichten, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
uploadschlange.py      angekommen, faellig, gleicher, nach_versuch, pause_s
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
werkzeugpfad.py        alter_tage, befund, lage, nachahmen_aus, pruefen, voranstellen
whispercfg.py          bedarf_mb, benutzt, entladen_wenn_leer, frei_mb, gebrauch, geladen, leerlauf_s, name, rss_hinweis, verfuegbar, waehle, wechsel_pruefen
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlparbeiter.py       main
ytdlpdienst.py         alle_beenden, anzahl, ausfuehren, laeufe_max, lage
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
zeitglaetter.py        ausdruck, bsf_args, filter_text, verfuegbar
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime, ohne_denkblock
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler, frische_intervalle
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
